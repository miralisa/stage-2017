# -*-coding:Latin-1 -*

from flask import Flask, render_template
from flaskext.mysql import MySQL
import json
import os
from elasticsearch import Elasticsearch

app = Flask(__name__)
mysql = MySQL()

file_ids = open("database_identifiers.json","r")
ids = json.load(file_ids)
file_ids.close()

app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_DATABASE_USER'] = str(ids['login'])
app.config['MYSQL_DATABASE_PASSWORD'] = str(ids['password'])
app.config['MYSQL_DATABASE_DB'] = str(ids['database_name'])
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

"""  
# Search test
def search(term):
	#analyzer = "'french': {'tokenizer': 'standard','filter': ['french_elision','lowercase', 'french_stop', 'french_keywords', 'french_stemmer' ]"
	res = es.search(index='index_decision', body={"query": {"query_string" : {"query": term, "fuzziness" : 1, "default_field": "contenu"}}, "size": 470, "highlight": {"fields" : {"contenu" : {}}}}) #{"query": { "fuzzy" : { "contenu" : { "value" : term, "fuzziness" : 2,}}}}) #{'query': {"fuzzy" : {'query_string' : {'default_field' : 'contenu', 'query' : term}}}})
	print('%d documents found' % res['hits']['total'])
	liste_id = []
	liste_highlights = []
	file = open("highlight.txt","w")

	for doc in res['hits']['hits']:
		liste_id.append(int(doc['_id']))
		liste_highlights.append(doc['highlight'])
		file.write(str(doc['highlight']) + "\n")

	file.close()  
	print liste_id

toSearch = "medecin"
keyWords = toSearch.split(" ")
paramToSearch = ''
print keyWords
for w in keyWords:
	if w == "AND" or w =="NOT" or w == "OR":
		paramToSearch += w + " "
	elif w[-1] == ")":
		nw = w[:-1]
		paramToSearch += nw + "~) "
	else:	
		paramToSearch += w + "~ "
print paramToSearch				
search(paramToSearch)

"""

#Put data to ES server
conn = mysql.connect()
cur=conn.cursor()
cur.execute('''SELECT id_decision, description from decision''')
allDec = cur.fetchall()
for dec in allDec:
	es.index(index='index_decision', doc_type='texte', id=dec[0], body={'contenu':dec[1]}, request_timeout=50)
