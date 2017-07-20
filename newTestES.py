# -*-coding:Latin-1 -*

from flask import Flask, render_template
from flaskext.mysql import MySQL
import csv, random
import pandas as pd
import os
import requests
from elasticsearch import Elasticsearch


app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'decisionsJustice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def search(term):
	#analyzer = "'french': {'tokenizer': 'standard','filter': ['french_elision','lowercase', 'french_stop', 'french_keywords', 'french_stemmer' ]"
	res = es.search(index='decisions', body={"query": {"query_string" : {"query": term, "default_field": "contenu"}}, "size": 470, "highlight": { "fields" : { "contenu" : {}}}}) #{"query": { "fuzzy" : { "contenu" : { "value" : term, "fuzziness" : 2,}}}}) #{'query': {"fuzzy" : {'query_string' : {'default_field' : 'contenu', 'query' : term}}}})
	print('%d documents found' % res['hits']['total'])
	liste_id = []
	liste_highlights = []
	for doc in res['hits']['hits']:
		liste_id.append(int(doc['_id']))
		liste_highlights.append(doc['highlight'])
	print liste_id

#res = requests.get('http://localhost:9200')
#print res.content

"""
Put date to ES server
conn = mysql.connect()
cur=conn.cursor()
cur.execute('''SELECT * from decision''')
allDec = cur.fetchall()
for dec in allDec:
	es.index(index='decisions', doc_type='texte', id=dec[0], body={'contenu':dec[5]})
"""

#print es.search(index='decisions', body={'query':{'bool':{'must':[{'fuzzy':{'contenu':{'value':'dommage AND voisinage'}}}]}}})
toSearch = "enterprise AND (dommage OR amende)"
keyWords = toSearch.split(" ")
paramToSearch = ''
print keyWords
for w in keyWords:
	if w == "AND" or w =="NOT" or w == "OR":
		paramToSearch += w + " "
	elif w[-1]==")":
		nw=w[:-1]
		paramToSearch += nw + "~) "
	else:	
		paramToSearch += w + "~ "
print paramToSearch				
search(paramToSearch)

"""
"query": {"query_string" : {"query": term, "default_field": "contenu"}}

curl -XPOST 'http://localhost:9200/decisions/_close'

curl -XPUT  'http://localhost:9200/decisions/' -d '{
  "settings": {
    "index": {
      "analysis": {
        "filter": {
          "stemmers": {
            "type": "stemmer",
            "language": "french"
                  }
            },
        "analyzer": {
          "filter_stemmer": {
            "filter": [
              "standard",
              "lowercase",
              "stemmers"
            ],
            "tokenizer": "standard"
                  }
            }
      }
    }
  }
}'

curl -XPOST 'http://localhost:9200/myindex/_open'

"highlight": { fields" : { "contenu" : {}}}

{"query": { "match": { "text": {"query": term,"fuzziness": "AUTO"}}}}

curl -XGET 'localhost:9200/_search?pretty' -H 'Content-Type: application/json' -d'
{
    "query": { "fuzzy" : { "user" : { "value" : term, "fuzziness" : 2,}}}
}
'

curl -XPUT 'localhost:9200/decisions?pretty' -d '
{
  'settings': {
    'analysis': {
      'filter': {
          'french_stop': {
          'type':       'stop',
          'stopwords':  '_french_' 
        },
          'french_stemmer': {
          'type':       'stemmer',
          'language':   'light_french'
        }
      },
      'analyzer': {
        'french': {'tokenizer':  'standard','filter': ['french_elision','lowercase', 'french_stop', 'french_keywords', 'french_stemmer' ]
        }
      }
    }
  }
}
"""
