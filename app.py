#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, Response, request, json
from flaskext.mysql import MySQL

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

	cur.execute('''SELECT distinct categorie from demande''')
	categories = cur.fetchall()

	#cur.execute('''SELECT distinct ville from decision''')
	cur.execute('''SELECT count(*), ville from decision group by ville''')

	villes = cur.fetchall()

	return render_template('index_test.html', data=data,categories=categories, villes=villes )

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
	categories = json.loads(request.args.get('categories'))
	quantumD = json.loads(request.args.get('quantumD'))
	quantumR = json.loads(request.args.get('quantumR'))
	resultat = json.loads(request.args.get('resultat'))
	search = {'villes':len(villes), 'categories':len(categories),  'quantumD':len(quantumD), 'quantumR':len(quantumR), 'resultat':len(resultat)}
	filters = []
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
			if 	len(filters) == 1:
				query2+="ville='"+villes[-1]+"')"
			else:
				query2+="ville='"+villes[-1]+"') AND "	
			
		if f == 'categories':
			query2+="("
			for c in categories[:-1]:
				query2+= "categorie=\""+c+ "\" OR "
			if ('quantumD' or 'quantumR') in filters:
				query2+= "categorie=\""+categories[-1]+ "\" AND "
			else:
				query2+="categorie=\""+categories[-1]+"\")"

		if f == 'resultat':
			query2+="("
			for r in resultat[:-1]:
				query2+= "resultat=\""+r+ "\" OR "
			if ('categories') in filters:
				query2+= "resultat=\""+resultat[-1]+ "\") AND "
			else:
				query2+="resultat=\""+resultat[-1]+"\")"
			
			#if 	len(filters) == 0:
			#query2+="resultat=\""+resultat[-1]+"\")"
			
	
			#else:
	query = '''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query2+''
	query0 = '''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision'''
	print filters
	print query2
	if len(filters) == 0:
		cur.execute(query0)
	else:	
		cur.execute(query)
	data = cur.fetchall()
	query2=''
	
	return jsonify(result=data)

	
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
	cur.execute('''SELECT count(*), categorie from demande group by categorie''')
	data = cur.fetchall()
	
	cur.execute('''SELECT count(*), ville from decision group by ville''')
	data_villes = cur.fetchall()

	cur.execute('''SELECT count(*), resultat from demande group by resultat''')
	data_resultat = cur.fetchall()
	
	categories = []
	children = []
	for result in data:
		#print result[2] 
		d = {'name': result[1], 'nb': result[0]}
		categories.append(d)
	ch = {'name':'Categorie', 'children':categories, 'nb':len(categories)}
	children.append(ch)
		
	villes = []
	for result in data_villes:
		#print result[2] 
		d = {'name': result[1], 'nb': result[0]}
		villes.append(d)
	v = {'name':'Ville','children':villes, 'nb':len(villes)}
	children.append(v)
		

	juridiction = []
	j = {'name':'Juridiction','children':juridiction, 'nb':len(juridiction)}
	children.append(j)
	
	resultats = []
	for result in data_resultat:
		d = {'name': result[1], 'nb': result[0]}
		resultats.append(d)

	r = {'name':'Resultat','children':resultats, 'nb':len(resultats)}
	children.append(r)
	
	
		

	return jsonify(name='Decisions', children=children)
	
if __name__ == '__main__':
	app.run(debug=True)
