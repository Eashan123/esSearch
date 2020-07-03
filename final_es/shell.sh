# In codes folder keep the code, in data keep the pdf to extract text.pip3.6 install --upgrade --no-cache-dir tensorflow

# Os is centos, if Ubuntu, replace yum with apt-get

#cd /usr/share/elasticsearch/
mkdir searchqa
cd searchqa
mkdir codes
mkdir data

yum -y update
yum install -y python3
yum install -y vim
yum -y install wget
yum clean all

pip3.6 install --upgrade pip
pip3.6 install elasticsearch
pip3.6 install pandas

# Ingest Plugin, use if os is linux else check the official website

/usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-attachment 


# Text embeddings
pip3.6 install --upgrade --no-cache-dir tensorflow
pip3.6 install --upgrade tensorflow-hub

# Install USE locally, change the model_path in config

pip3.6 install flask

# Text Summarization
pip3 install transformers==2.8.0
pip3 install torch==1.4.0






