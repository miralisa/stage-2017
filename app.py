#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, Response, request, json
from flaskext.mysql import MySQL
import random

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


@app.route('/')
def index():
	cur = conn.cursor()
	cur.execute('''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision''')
	data = cur.fetchall()

	cur.execute('''SELECT count(*), categorie from demande group by categorie''')
	categories = cur.fetchall()

	#cur.execute('''SELECT distinct ville from decision''')
	cur.execute('''SELECT count(*), ville from decision group by ville''')

	villes = cur.fetchall()

	return render_template('index_test.html', data=data, categories=categories, villes=villes )

@app.route('/index')
def mindex():
	cur = conn.cursor()
	cur.execute('''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision''')
	data = cur.fetchall()

	cur.execute('''SELECT distinct categorie from demande''')
	categories = cur.fetchall()

	cur.execute('''SELECT distinct ville from decision''')
	villes = cur.fetchall()

	return render_template('index.html', data=data,categories=categories, villes=villes )

@app.route('/searchByCity/')
def get_villes():
	#villes = request.args.get('villes', 0, type=str)
	villes = json.loads(request.args.get('villes'))
	cur = conn.cursor()
	
	query2 = ''

	for v in villes[:-1]:
		query2+= "ville='"+v+ "' OR "
	query2+="ville='"+villes[-1]+"'"
	query1 = '''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query2+''

	cur.execute(query1)
	data = cur.fetchall()
	return jsonify(result=data)

@app.route('/search/')
def get_results():
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
			#SELECT description FROM decision WHERE MATCH(description) AGAINST('Agen');
			if filters[-1] == 'texte':
				query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE))"
			else:
				query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE)) AND "	
		

	
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
	query = '''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query2+''
	query0 = '''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision'''

	#queryVilles = '''SELECT  count(*), ville FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query2+ '''group by ville'''
	queryCategorie = '''SELECT  count(*) as nb_categorie, categorie FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query2+ ''' group by categorie order by nb_categorie desc'''


	print filters
	print query2

	data_categories = []

	if len(filters) == 0:
		cur.execute(query0)
	else:
		cur.execute(queryCategorie)
		data_categories = cur.fetchall()
	
		cur.execute(query)
	data = cur.fetchall()
	#query2=''

	print data_categories

	categories = []
	children = []

	for res in data_categories:
		#print result[2] 
		
		query3 = query2+ " AND categorie=\""+res[1]+"\" group by resultat order by nb_res desc"
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
	query2=''
	
	#build_tree(data)
	if len(data_categories) != 0:
		return jsonify(result=data, name='Filtres', children=children)
	else:
		return jsonify(result=data)

def build_tree(data):
	print 'coucou'
"""	
	categories = []
	children = []
	for result in data:
		#print result[2] 
		d = {'name': result[1], 'nb': result[0]}
		categories.append(d)
	ch = {'name':'Catégories', 'children':categories, 'nb':len(categories)}
	children.append(ch)

	for d in data:
		jd = {'name': d[2], 'nb': result[0]} 
"""
		
	
@app.route('/dashboard/')
def dashboard():
	return render_template('dashboard.html')

@app.route('/testd3/')
def testd3():
	file = open("./input/flare.json","r")
	#print file.read()
	return file.read()


@app.route('/all_decisions/')
def all_decisions():
	cur = conn.cursor()
	#cur.execute('''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision''')
	cur.execute('''SELECT count(*) as nb_categorie, categorie from demande group by categorie order by nb_categorie desc''')
	data = cur.fetchall()
	
	cur.execute('''SELECT count(*) as nb_ville, ville from decision group by ville order by nb_ville desc''')
	data_villes = cur.fetchall()

	cur.execute('''SELECT count(*) as nb_res, resultat from demande group by resultat order by nb_res desc''')
	data_resultat = cur.fetchall()
	

	categories = []
	children = []
	tree2_children = []
	chJuridiction = []
	chCategories = []

	juridiction = []
	j = {'name':'Juridictions','children':juridiction, 'color':colors()}#, 'nb':len(juridiction)}
	children.append(j)

	children.append({'name':'Date', 'children':[], 'color':colors()})
	
	for result in data:
		#print result[2] 
		query3 = "categorie=\""+result[1]+"\" group by resultat order by nb_res desc"
		queryResultat = '''SELECT  count(*) as nb_res, resultat FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query3+''
	
		cur.execute(queryResultat)
		data_resultats = cur.fetchall()
		
		resultats = []
		for results in data_resultats:
			if results[1] == 'accepte':	
				color = 'green'
			elif  results[1] == 'rejette': 
				color = 'red'
			else:
				color ='yellow'
			r = {'name': results[1], 'nb': results[0], 'color':color}
			resultats.append(r)	

		d = {'name': result[1], 'nb': result[0], 'color':colors(), 'children':resultats}
		categories.append(d)
	
	ch = {'name':'Catégories', 'children':categories, 'color':colors()} #, 'nb':len(categories)}
	tree2_children.append(ch)
	
	
	villes = []
	for result in data_villes:
		#print result[2] 
		d = {'name': result[1], 'nb': result[0],  'color':colors()}
		villes.append(d)
		#query2 +=  "ville = \"" + result[1] + "\""
		#queryCategorie = '''SELECT  count(*) as nb_categorie, categorie FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query2+ ''' group by categorie order by nb_categorie desc'''
		#cur.execute(queryCategorie)

	
	v = {'name':'Villes','children':villes, 'color':colors()}#, 'nb':len(villes)}
	children.append(v)
		
	#juridiction.append({'name':'Villes', 'children':villes})
	
	
	resultats = []
	for result in data_resultat:
		if result[1] == 'accepte':	
			color = 'green'
		elif  result[1] == 'rejette': 
			color = 'red'
		else:
			color ='yellow'		
		d = {'name': result[1], 'nb': result[0], 'color':color}
		resultats.append(d)

	r = {'name':'Resultats','children':resultats,'parent':'Filtres', 'color':colors()}#, 'nb':len(resultats)}
	children.append(r)
	
	terms = {'name':'Terms','children':[],'parent':'Filtres', 'color':colors()}#, 'nb':len(resultats)}
	children.append(terms)
	
	tree_root2 = {'name':'Filtres','children':children, 'color':colors(), "parent": "null"}	
	tree_root = {'name':'Filtres','children':tree2_children, 'color':colors(), "parent": "null"}	

	return jsonify(tree=tree_root, tree2=tree_root2)

def colors():
	colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"]
	return colores_g[random.randint(0,len(colores_g)-1)]
	
if __name__ == '__main__':
	app.run(debug=True)
