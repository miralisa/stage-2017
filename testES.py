#!/usr/bin/env python
# coding: utf-8

import requests
from elasticsearch import Elasticsearch
from flask import Flask, render_template, jsonify, Response, request, json
from flaskext.mysql import MySQL
import random, time

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'decisionsJustice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['MYSQL_USE_UNICODE'] = 'False'
app.config['MYSQL_CHARSET'] = 'utf-8'
mysql.init_app(app)

conn = mysql.connect()

def colors():
	colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"]
	return colores_g[random.randint(0,len(colores_g)-1)]

@app.route('/all_decisions/')
def all_decisions():
	print time.time()
	cur = conn.cursor()
	children = []
	
	""" Request all cities in database """	
	cur.execute('''SELECT count(*) as nb_ville, ville from decision JOIN demande ON decision.id_decision = demande.id_decision group by ville ''')
	data_villes = cur.fetchall()

	
	villes = []
	""" For each city select categories """
	for result in data_villes:
		query =  "ville = \"" + result[1] + "\""
		queryCategorie = '''SELECT count(*) as nb_categorie, objet from decision, demande, categorie WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND
'''+query+ ''' group by objet order by nb_categorie desc'''
		cur.execute(queryCategorie)
		categorieParVille = cur.fetchall()
		resultats = []

		""" For each categories in the same city select norme """
		for c in categorieParVille:
			query3 = "ville = \"" + result[1] + "\" AND objet=\""+c[1]+"\" group by norme order by nb_res desc"
			queryResultat = '''SELECT  count(*) as nb_res, norme from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query3+''
			cur.execute(queryResultat)
			normeParCat = cur.fetchall()
			
			normeParCatChildren = []
			
			""" For each norme in the same city and category select resultats """
			for res in normeParCat:
				query4 = "ville = \"" + result[1] + "\" AND objet=\""+c[1]+"\" AND norme=\""+res[1]+"\" group by resultat order by nb_res desc"
				queryResultats = '''SELECT  count(*) as nb_res, resultat from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query4+''
				cur.execute(queryResultats)
				resParNorme = cur.fetchall()
				
				""" For each resultat put """
				resParNormeChildren = []
				for r in resParNorme:
					if r[1] == 'accepte':	
						color = 'green'
					elif  r[1] == 'rejette': 
						color = 'red'
					else:
						color ='yellow'
					d = {'name': r[1], 'nb': r[0],'tree':'Resultats', 'color':color}
					resParNormeChildren.append(d)
		
				d = {'name': res[1], 'nb': res[0],'children':resParNormeChildren,'tree':'Normes', 'color':colors()}
				normeParCatChildren.append(d)

			r = {'name': c[1], 'nb': c[0], 'children':normeParCatChildren,'tree':'Categories', 'color':colors()}
			resultats.append(r)
			
			
		d = {'name': result[1], 'nb': result[0], 'tree':'Villes', 'children': resultats,  'color':colors()}
		villes.append(d)
			
	v = {'name':'Villes','children':villes,'nb': 655, 'tree':"Filtres", 'color':colors()}#, 'nb':len(villes)}
	children.append(v)

	tree_root = {'name':'Filtres','children':children, 'color':colors(), "parent": "null"}	
	return jsonify(tree=tree_root)

@app.route('/')
def index():
	cur = conn.cursor()

	#cur.execute('''SELECT  * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme ''')
	#data = cur.fetchall()

	cur.execute('''SELECT count(*) as nb_categorie, objet from categorie JOIN demande ON categorie.id_categorie = demande.id_categorie group by objet order by nb_categorie desc''')
	categories = cur.fetchall()

	#cur.execute('''SELECT distinct ville from decision''')
	cur.execute('''SELECT count(*) as nb_ville, ville from decision group by ville''')

	villes = cur.fetchall()

	return render_template('index_test.html', categories=categories, villes=villes )

def define_filtres():
	villes = json.loads(request.args.get('villes'))
	date = json.loads(request.args.get('date'))
	categories = json.loads(request.args.get('categories'))
	quantumD = json.loads(request.args.get('quantumD'))
	quantumR = json.loads(request.args.get('quantumR'))
	resultat = json.loads(request.args.get('resultat'))
	juridiction =  json.loads(request.args.get('juridiction'))
	texte =  json.loads(request.args.get('texte'))
	search = {'date':len(date), 'juridiction':len(juridiction), 'texte':len(texte), 'villes':len(villes), 'categories':len(categories),  'quantumD':len(quantumD), 'quantumR':len(quantumR), 'resultat':len(resultat)}
	filters = []
	# search = {'quantumD': 0, 'resultat': 0, 'quantumR': 0, 'texte': 0, 'date': 2, 'juridiction': 0, 'villes': 1, 'categories': 0}

	for key, value in search.iteritems():
		if value>0:
			filters.append(key)
	
	cur = conn.cursor()
	

	query2 = ''
		
	for f in filters:
		if f == 'villes':
			query2+="("
			for v in villes[:-1]:
				query2+= "ville='"+v+ "' OR "
			if filters[-1] == 'villes':
				query2+="ville='"+villes[-1]+"')"
			else:
				query2+="ville='"+villes[-1]+"') AND "	
		
		if f == 'date':
			cond = str(date[0])
			if cond =="a":
				query2+="("
				for d in date[1:-1]:
					query2+= "date_decision='"+d+ "' OR "
				if 	filters[-1] == 'date':
					query2+="date_decision='"+date[-1]+"')"
				else:
					query2+="date_decision='"+date[-1]+"') AND "
			elif cond == "entre":
				if 	filters[-1] == 'date':
					query2+="( date_decision BETWEEN '"+date[2]+"' AND '"+ date[1] +"' )"
				else:
					query2+="( date_decision BETWEEN '"+date[2]+"' AND '"+ date[1] +"' ) AND "
			elif cond == "avant":
				if 	filters[-1] == 'date':
					query2+="( date_decision < '"+date[1] +"' )"
				else:
					query2+="( date_decision < '"+date[1] +"' ) AND "
			elif cond == "apres":
				if 	filters[-1] == 'date':
					query2+="( date_decision > '"+date[1] +"' )"
				else:
					query2+="( date_decision > '"+date[1] +"' ) AND "
				
		if f == 'texte':
			keyWords = texte.split(" ")
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
			print time.time()		
			es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
			res = es.search(index='decisions', body={"query": {"query_string" : {"query": paramToSearch, "fuzziness" : 2, "default_field": "contenu"}}, "size": 470, "highlight": { "fields" : { "contenu" : {}}}})
			print('%d documents found' % res['hits']['total'])
			print time.time()
			liste_id = []
			#dict_highlights = {}
			for doc in res['hits']['hits']:
				liste_id.append(int(doc['_id']))
			liste_ids = str(liste_id)[1:-1]

			if filters[-1] == 'texte':
				query2+="decision.id_decision IN ( " + liste_ids +" ) "
			else:
				query2+="decision.id_decision IN ( " + liste_ids +" ) AND "	
				
			"""
			if filters[-1] == 'texte':
				query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE))"
			else:
				query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE)) AND "	
			"""

	
		if f == 'categories':
			query2+="("
			for c in categories[:-1]:
				query2+= "categorie=\""+c+ "\" OR "
			if filters[-1] != 'categories':
				query2+= "categorie=\""+categories[-1]+ "\" AND "
			else:
				query2+="categorie=\""+categories[-1]+"\")"

		if f == 'resultat':
			query2+="("
			for r in resultat[:-1]:
				query2+= "resultat=\""+r+ "\" OR "
			if filters[-1] != 'resultat':
				query2+= "resultat=\""+resultat[-1]+ "\") AND "
			else:
				query2+="resultat=\""+resultat[-1]+"\")"
			
			#if 	len(filters) == 0:
			#query2+="resultat=\""+resultat[-1]+"\")"
			
	
			#else:
	return query2		


@app.route('/show_text/')
def show_text():
	query2 = define_filtres()
	query = ''
	queryNB = ''
	print len(query2)
	if len(query2) != 0:
		query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query2+' GROUP BY rg ORDER BY ville LIMIT 0, 15 '
		queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme  AND '''+query2+' GROUP BY rg ORDER BY ville'
	else:
		query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme GROUP BY rg ORDER BY ville LIMIT 0, 15'''
		queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme GROUP BY rg ORDER BY ville'''
	
	cur = conn.cursor()
	cur.execute(queryNB)
	nbDem = cur.fetchall()
	nbPage = len(nbDem)/15
	cur.execute(query)
	data = cur.fetchall()
	return jsonify(result=data, nbPage=nbPage)
	

@app.route('/show_page/')
def show_page():
	numPage = json.loads(request.args.get('numPage')) 
	query2 = define_filtres()
	query = ''
	queryNB = ''
	if len(query2) != 0:
		query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query2+' GROUP BY rg ORDER BY ville LIMIT '''+ str(int(numPage)*15) +', 15'
		#queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme  AND '''+query2+' GROUP BY rg '''
	else:
		query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme GROUP BY rg ORDER BY ville LIMIT '''+ str(int(numPage)*15) +", 15"
		#queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme GROUP BY rg '''
	
	cur = conn.cursor()
	#cur.execute(queryNB)
	#nbDem = cur.fetchall()
	#nbPage = len(nbDem)/15
	cur.execute(query)
	data = cur.fetchall()
	return jsonify(result=data)


@app.route('/search/')
def get_results():
	query2 = define_filtres()
	cur = conn.cursor()
	

	queryCategorie = '''SELECT count(*) as nb_categorie, objet from decision, demande, categorie WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND
'''+query2+ ''' group by objet order by nb_categorie desc'''
	data_categories = []
	
	if len(query2) == 0:
		queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme '''
	else:
		queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme  AND '''+query2
		cur.execute(queryCategorie)
		data_categories = cur.fetchall()
	cur.execute(queryNB)	
	data = cur.fetchall()

	categories = []
	children = []

	for res in data_categories:
		#print result[2] 
		query3 = query2+ " AND objet=\""+res[1]+"\" group by norme order by nb_res desc"
		queryResultat = '''SELECT  count(*) as nb_res, norme from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query3+''
		#print queryResultat

		cur.execute(queryResultat)
		data_resultats = cur.fetchall()
		
		resultats = []
		for results in data_resultats:
			query4 =  query2+" AND objet=\""+res[1]+"\" AND norme=\""+results[1]+"\" group by resultat order by nb_res desc"
			queryResultats = '''SELECT  count(*) as nb_res, resultat from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query4+''
			cur.execute(queryResultats)
			resParNorme = cur.fetchall()
			
			#print resParNorme
			resParNormeChildren = []
			for r in resParNorme:
				if r[1] == 'accepte':	
					color = 'green'
				elif  r[1] == 'rejette': 
					color = 'red'
				else:
					color ='yellow'
				d = {'name': r[1], 'nb': r[0],'tree':'Resultats', 'color':color}
				resParNormeChildren.append(d)
			
			r = {'name': results[1],'color':colors(),'children':resParNormeChildren,'tree':'Normes', 'nb': results[0]}
			resultats.append(r)
			#print r


		d = {'name': res[1], 'nb': res[0],'color':colors(),'tree':'Categories', 'children':resultats}
		categories.append(d)

	ch = {'name':'Catégories', 'children':categories,'color':colors(),'tree':'Categories', 'nb':data[0][0]}
	children.append(ch)
	query2=''
	
	#build_tree(data)
	if len(data_categories) != 0:
		tree_root = {'name':'Filtres','children':children, 'nb':data[0][0],'color':colors(), "parent": "null"}
		print time.time()
		return jsonify(tree=tree_root)
	

@app.route('/filtres/')
def get_resultats():
	villes = json.loads(request.args.get('villes'))
	date = json.loads(request.args.get('date'))
	categories = json.loads(request.args.get('categories'))
	quantumD = json.loads(request.args.get('quantumD'))
	quantumR = json.loads(request.args.get('quantumR'))
	resultat = json.loads(request.args.get('resultat'))
	juridiction =  json.loads(request.args.get('juridiction'))
	texte =  json.loads(request.args.get('texte'))
	search = {'date':len(date), 'juridiction':len(juridiction), 'texte':len(texte), 'categories':len(categories),  'quantumD':len(quantumD), 'quantumR':len(quantumR), 'resultat':len(resultat)} #'villes':len(villes),
	filters = []
	# search = {'quantumD': 0, 'resultat': 0, 'quantumR': 0, 'texte': 0, 'date': 2, 'juridiction': 0, 'villes': 1, 'categories': 0}

	for key, value in search.iteritems():
		if value>0:
			filters.append(key)
	
	cur = conn.cursor()
	

	query2 = ''
	
	for f in filters:
		"""
		if f == 'villes':
			query2+="("
			for v in villes[:-1]:
				query2+= "ville='"+v+ "' OR "
			if filters[-1] == 'villes':
				query2+="ville='"+villes[-1]+"')"
			else:
				query2+="ville='"+villes[-1]+"') AND "	
		"""
		if f == 'date':
			cond = str(date[0])
			if date[1]!="":	
				if cond =="a":
					query2+="("
					for d in date[1:-1]:
						query2+= "date_decision='"+d+ "' OR "
					if 	filters[-1] == 'date':
						query2+="date_decision='"+date[-1]+"')"
					else:
						query2+="date_decision='"+date[-1]+"') AND "
				elif cond == "entre":
					if 	filters[-1] == 'date':
						query2+="( date_decision BETWEEN '"+date[2]+"' AND '"+ date[1] +"' )"
					else:
						query2+="( date_decision BETWEEN '"+date[2]+"' AND '"+ date[1] +"' ) AND "
				elif cond == "avant":
					if 	filters[-1] == 'date':
						query2+="( date_decision < '"+date[1] +"' )"
					else:
						query2+="( date_decision < '"+date[1] +"' ) AND "
				elif cond == "apres":
					if 	filters[-1] == 'date':
						query2+="( date_decision > '"+date[1] +"' )"
					else:
						query2+="( date_decision > '"+date[1] +"' ) AND "
				
		if f == 'texte':
			
			keyWords = texte.split(" ")
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
			print time.time()		
			es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
			res = es.search(index='decisions', body={"query": {"query_string" : {"query": paramToSearch, "fuzziness" : 2, "default_field": "contenu"}}, "size": 470, "highlight": { "fields" : { "contenu" : {}}}})
			print('%d documents found' % res['hits']['total'])
			print time.time()
			liste_id = []
			#dict_highlights = {}
			for doc in res['hits']['hits']:
				liste_id.append(int(doc['_id']))
				"""	
				if 'highlight' in doc:
					content = doc['highlight']['contenu']
					dict_highlights.update({doc['_id']: content})
				"""
			liste_ids = str(liste_id)[1:-1]
			"""
			query2+=" ("
			for el in liste_id[:-1]:
				query2+=" decision.id_decision = "+str(el)+" OR "
			if filters[-1] == 'texte':
				query2+=" decision.id_decision = "+str(el)+" ) "
			else:
				query2+=" decision.id_decision = "+str(el)+" ) AND "
			"""
			if filters[-1] == 'texte':
				query2+="decision.id_decision IN ( " + liste_ids +" ) "
			else:
				query2+="decision.id_decision IN ( " + liste_ids +" ) AND "	
						
			"""
			if filters[-1] == 'texte':
				query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE))"
			else:
				query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE)) AND "	
			"""
		

		""" categorie = objet
		if f == 'categories':
			query2+="("
			for c in categories[:-1]:
				query2+= "categorie=\""+c+ "\" OR "
			if filters[-1] != 'categories':
				query2+= "categorie=\""+categories[-1]+ "\" AND "
			else:
				query2+="categorie=\""+categories[-1]+"\")"
		"""
		if f == 'resultat':
			query2+="("
			for r in resultat[:-1]:
				query2+= "resultat=\""+r+ "\" OR "
			if filters[-1] != 'resultat':
				query2+= "resultat=\""+resultat[-1]+ "\") AND "
			else:
				query2+="resultat=\""+resultat[-1]+"\")"
			
			#if 	len(filters) == 0:
			#query2+="resultat=\""+resultat[-1]+"\")"
			
			#else:
	#print query2		
	query = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme  AND '''+query2
	query0 = '''SELECT demande.id_demande from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme'''

	queryCategorie = '''SELECT count(*) as nb_categorie, objet from decision, demande, categorie WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND
'''+query2+ ''' group by objet order by nb_categorie desc'''


	#print filters
	#print query2
	
	data_categories = []

	if len(query2) == 0:
		cur.execute(query0)
	else:
		cur.execute(query)
	data = cur.fetchall()
	#query2=''

	"""
	print data_categories

	categories = []
	children = []

	for res in data_categories:
		#print result[2] 
		
		query3 = query2+ " AND categorie=\""+res[1]+"\" group by resultat order by nb_res"
		queryResultat = '''SELECT  count(*) as nb_res, resultat FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query3+''
		print queryResultat

		cur.execute(queryResultat)
		data_resultats = cur.fetchall()
		
		resultats = []
		for results in data_resultats:
			r = {'name': results[1], 'nb': results[0]}
			resultats.append(r)
			print r

		d = {'name': res[1], 'nb': res[0], 'children':resultats}
		categories.append(d)

	ch = {'name':'Catégories', 'children':categories, 'nb':len(categories)}
	children.append(ch)
	"""

	# NEW TREE 
	

	tree_children = []
	villes_res = []
	nbDemande = 0

	if len(villes) < 34:
		queryVille = '('
		for v in villes[:-1]:
			queryVille +=  "ville = \"" + v+"\" OR "
		if len(query2) != 0:
			queryVille += "ville = \""+villes[-1]+"\" ) AND "+ query2
		else:
			queryVille += "ville = \""+villes[-1]+"\" )"
		#print queryVille

		queryRes = '''SELECT demande.id_demande from decision USE INDEX (iville), demande, categorie, norme  WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND'''+queryVille+''
		#print queryRes
		cur.execute(queryRes)
		data = cur.fetchall()

	#print len(villes)

	query2CatViile = ''
	if len(query2) != 0:
		query2CatViile=query2+ " AND "
	#print query2CatViile
	
	for v in villes[:]:
		if len(query2) != 0:
			query =  "ville = \"" + v + "\" AND "+ query2
		else:
			query =  "ville = \"" + v + "\" "
		queryNbDemande = '''SELECT  count(*) as nb_d FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query+''
		queryCategorie = '''SELECT count(*) as nb_categorie, objet from decision, demande, categorie USE INDEX (iobjet) WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND '''+query+ ''' group by objet order by nb_categorie desc'''
		#print queryCategorie
		cur.execute(queryCategorie)
		categorieParVille = cur.fetchall()

		#print len(categorieParVille)
		if len(categorieParVille)>0:
			cur.execute(queryNbDemande)
			nb = cur.fetchall()
			#print str(nb[0][0])
			nbDemande+=int(str(nb[0][0]))	
		
			
			
			resultatsCat = []
			for c in categorieParVille:
				query3 = query2CatViile+" ville = \"" + v + "\" AND objet=\""+c[1]+"\" group by norme order by nb_res desc"
				queryResultat = '''SELECT  count(*) as nb_res, norme from decision USE INDEX (iville), demande, categorie, norme USE INDEX (inorme) WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query3+''
				cur.execute(queryResultat)
				normeParCat = cur.fetchall()
				
				normeParCatChildren = []
				
				for res in normeParCat:
					query4 =  query2CatViile+" ville = \"" + v + "\" AND objet=\""+c[1]+"\" AND norme=\""+res[1]+"\" group by resultat order by nb_res desc"
					queryResultats = '''SELECT  count(*) as nb_res, resultat from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query4+''
					cur.execute(queryResultats)
					resParNorme = cur.fetchall()
					
					#print resParNorme
					resParNormeChildren = []
					for r in resParNorme:
						if r[1] == 'accepte':	
							color = 'green'
						elif  r[1] == 'rejette': 
							color = 'red'
						else:
							color ='yellow'
						d = {'name': r[1], 'nb': r[0],'tree':'Resultats', 'color':color}
						resParNormeChildren.append(d)
			
					d = {'name': res[1], 'nb': res[0],'children':resParNormeChildren,'tree':'Normes', 'color':colors()}
					normeParCatChildren.append(d)

				r = {'name': c[1], 'nb': c[0], 'children':normeParCatChildren,'tree':'Categories', 'color':colors()}
				resultatsCat.append(r)

			d = {'name': v, 'nb': nb[0], 'tree':'Villes', 'children': resultatsCat,  'color':colors()}
			villes_res.append(d)
		 
	v = {'name':'Villes','children':villes_res, 'nb':nbDemande, 'tree':"Filtres", 'color':colors()}#, 'nb':len(villes)}
	
	tree_children.append(v)

	tree_root = {'name':'Filtres','children':tree_children, 'color':colors(), "parent": "null"}
	print time.time()
	return jsonify(result=data, tree=tree_root)


if __name__ == '__main__':
	app.run(debug=True, port=5555)
