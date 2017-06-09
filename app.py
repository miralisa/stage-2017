#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, Response
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
