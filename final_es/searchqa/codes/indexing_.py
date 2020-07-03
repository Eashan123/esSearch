import tensorflow as tf
from elasticsearch import Elasticsearch
import base64
import json
import glob
import pandas as pd
from elasticsearch.helpers import bulk
import config as config
from copy import deepcopy
import re
import torch
import tensorflow_hub as hub
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import re

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

if es.ping():
        print('Connected to ES!')
else:
        print('Could not connect!')
        sys.exit()


# Defining T5 model:

device = torch.device('cpu')
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

pdf_dir = config.path_pdf
pdf_files = glob.glob("%s/*.pdf" % pdf_dir)

encoded_pdf = []

for i in pdf_files:
    with open(i, "rb") as pdf_file:
        encoded_pdf.append(base64.b64encode(pdf_file.read()).decode('ascii'))


# Deleting index corpus
es.indices.delete(index=config.index_name, ignore=[400, 404])


# Defining the pipeline

body = {
  "description" : "Extract attachment information",
  "processors" : [
    {
      "attachment" : {
        "field" : "data"
      }
    }
  ]
}

es.index(index='_ingest', doc_type='pipeline', id='attachment', body=body)

# Indexing

cnt = 0
for i in range(0, len(encoded_pdf)):
    rs = es.index(index=config.index_name,doc_type='pdf', pipeline = 'attachment', id=cnt, body={'data': encoded_pdf[i]})
    cnt +=1

lis = []
for i in range(cnt):
    lis.append( es.get(index=config.index_name,doc_type='pdf',id=i))

# Extracting data

doc = []

for it in lis:
    for k,v in it.items():
        if k == '_source':
            temp = v

            for k_, v_ in temp.items():
                if k_ == 'attachment':
                    temp_ = v_
                    doc.append(temp_)

# Data preprocessing:

def regular_exp(text):
    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    text = re.sub(r'[\n|\"|,|!]', r"", text)
    text = _RE_COMBINE_WHITESPACE.sub(" ", text).strip()
    return text

doc_ = deepcopy(doc)


cnt = 0
for i in doc_:
    for k,v in i.items():
        if k == 'content':
            #print(doc[cnt], '\n')
            doc_[cnt][k] = regular_exp(v)
            #print('true')
    cnt += 1

# To save compute time and space we will just work with content

lis = []
for i in doc_:
    for k, v in i.items():
        if k == 'content':
            lis.append(v)

# Extracted data from pdf into csv

df = pd.DataFrame(lis, columns = ['Content'])
df.to_csv(config.path_save)

# Summarizing text:

t5_prepared_Text = ["summarize: "+regular_exp(i) for i in lis]
tokenized_text = [tokenizer.encode(i, return_tensors="pt").to(device) for i in t5_prepared_Text]
summary_ids = [model.generate(i, num_beams=3, min_length=50, max_length=300, early_stopping=True) for i in tokenized_text]

liss = [tokenizer.decode(i[0], skip_special_tokens=True) for i in summary_ids]

# Summarized data into csv

df_ = pd.DataFrame(liss, columns = ['Summarized'])
df_.to_csv(config.path_summr)


print('content index file done \n')
es.indices.delete(index=config.index_name, ignore=[400, 404])


# Defining the pipeline

b = {"mappings": {"properties": {"content": {"type": "text"}, "content_vector": {"type": "dense_vector", "dims": 512}}}}


ret = es.indices.create(index= config.new_index, ignore=400, body=b) #400 caused by IndexAlreadyExistsException, 

embed = hub.load(config.model_path)

cnt = 0
for i in liss:
    doc_id = cnt
    content = i
    vec = tf.make_ndarray(tf.make_tensor_proto(embed([content]))).tolist()[0]
    b = {"content":content,
        "content_vector":vec}
    res = es.index(index=config.new_index, id=doc_id, body=b)
    cnt += 1
    print("Completed indexing....")        
