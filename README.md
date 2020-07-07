# esSearch

The packages to be installed could be found in shell script.

The Os used - Cent Os.

# High Level Design.

1. Setting up a docker as a virtual container.

2. Configuring CentOS

3. Integrating ES and low level Python API.

4. Use ingest plugin, a part of elasticstack.

5. Extract contents from pdf.

	{
		meta: {'author': Sole,
			'date': 22/03/2019,
			'type': pdf},
		content: { xyz}
	}

4. Preprocess content, remove special characters: Regular expressions.

5. Summarize text, Text-Text Transformer.

6. Create a custom map for fields you choose, relational schema.

7. Perform Indexing.

############################################

ETL

############################################

Approach 1: keyword

1. Feed indexed text to Es(), internally text is tf-idf vectorized.

2. Add boosting to give more weight to a field of more importance.


Approach 2: Semantic

1. Use Transfer learning to embed text.

2. Make a custom schema or map of text and its embeddings.

3. Index custom schema.

4. Add boosting to give more weight to a field of more importance.


##############################################

Indexing

##############################################

1. Use DSL query, match, multimatch.

2. Use booster to give more weights when more than one field is involved.

###############################################

Searching

###############################################

1. REST- Code.

2. Shell Script.
