from flask import Flask, render_template
from flaskext.mysql import MySQL
import csv

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'decisionsJustice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

insDecision = """INSERT INTO decision (rg, ville, juridiction, description) values (%s,%s,%s,"description")"""
insDemande = """INSERT INTO  demande (id_decision, quantum_demande, quantum_resultat, categorie, resultat) values (%s,%s,%s,%s,%s)"""

cur=conn.cursor()
cr = csv.reader(open("decisions.csv","rb"))

count = 1
next(cr)
for row in cr:
	if (str(row[3])=="x" or str(row[3])==" " or str(row[3])=="" or str(row[3])=="Faux positif DI" or str(row[3])=="error" or str(row[11])=="" or str(row[11])==" " or str(row[11])=="irrecevable" ):
		#if (str(row[7]))!="-" or (str(row[7]))!="?" or (str(row[13]))!="-" or (str(row[13]))!="?":
		print str(row[1]).lower().capitalize()
	else:	
		print count
		cur.execute(insDecision, ((str(row[2])), str(row[1]).lower().capitalize(), (str(row[0]))))
		cur.execute(insDemande, (count,(str(row[7])),(str(row[13])),(str(row[3])),(str(row[11]))))
		count+=1
		conn.commit()

