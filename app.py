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
			if 	len(filters) == 0:
				query2+="ville='"+villes[-1]+"')"
			else:
				query2+="ville='"+villes[-1]+"') AND "	
			
		if f == 'categories':
			query2+="("
			for c in categories[:-1]:
				query2+= "categorie=\""+c+ "\" OR "
			if ('quantumD' or 'quantumR' or 'resultat') in filters:
				query2+= "categorie=\""+categories[-1]+ "\" AND "
			else:
				query2+="categorie=\""+categories[-1]+"\")"

		if f == 'resultat':
			query2+="("
			for r in resultat[:-1]:
				query2+= "resultat=\""+r+ "\" OR "
			#if 	len(filters) == 0:
			query2+="resultat=\""+resultat[-1]+"\")"
			
	
			#else:
	query = '''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision WHERE '''+query2+''
	print filters
	print query2
	
	cur.execute(query)
	data = cur.fetchall()
	query2=''
	
	return jsonify(result=data)

	
#@app.route('/test/')
def all_decisions():
	cur = conn.cursor()
	cur.execute('''SELECT * FROM decision JOIN demande ON decision.id_decision = demande.id_decision''')
	data = cur.fetchall()
	
	json_results = []
	for result in data:
		#print result[2] 
		d = {'id': result[0], 'rg': result[1], 'ville': result[2], 'juridiction': result[3], 'description': result[4], 'quantum_demande': result[6],'quantum_resultat': result[7],'categorie': result[8],'resultat': result[9]}
		json_results.append(d)
	return data#jsonify(decisions=json_results)

if __name__ == '__main__':
	app.run(debug=True)
