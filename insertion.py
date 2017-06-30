from flask import Flask, render_template
from flaskext.mysql import MySQL
import csv, random
import pandas as pd
import os


app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'decisionsJustice'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

insDecision = """INSERT INTO decision (rg, ville, date_decision, juridiction, description) values (%s,%s,%s,%s,%s)"""
insDemande = """INSERT INTO  demande (quantum_demande, quantum_resultat, categorie, resultat, id_decision) values (%s,%s,%s,%s,%s)"""

cur=conn.cursor()
cr = csv.reader(open("res_dec.csv","rb"))
#writer = csv.writer(open('output.csv', 'w'))

files_content = []
for filename in os.listdir("/home/anastasiia/Documents/stage/decision-de-justice"):
	f = open("/home/anastasiia/Documents/stage/decision-de-justice/"+filename, "rb")
	files_content.append(f.read())
	print files_content




count = 0
tab_count = []
next(cr)
rg = ''
for row in cr:
	if str(row[15])!="0":
		cur.execute(insDemande, ((str(row[7])),(str(row[13])),(str(row[3])),(str(row[11])), row[15]))
		conn.commit()	
		
	"""
	if (str(row[3])=="x" or str(row[3])==" " or str(row[3])=="" or str(row[3])=="Faux positif DI" or str(row[3])=="error" or str(row[11])=="" or str(row[11])==" " or str(row[11])=="  " or str(row[11])=="irrecevable" ):
		#if (str(row[7]))!="-" or (str(row[7]))!="?" or (str(row[13]))!="-" or (str(row[13]))!="?":
		tab_count.append(0)
		print str(row[1]).lower().capitalize()
	else:
		print row[15]
		
		if str(row[2])==rg:
			print rg
			tab_count.append(count)
			#cur.execute(insDemande, ((str(row[7])),(str(row[13])),(str(row[3])),(str(row[11])), count))			
			#conn.commit()
			
		else:
			count+=1
			tab_count.append(count)
			year = random.randint(2000,2017)
			day = random.randint(1,31)
			month = random.randint(1,12)
			cur.execute(insDecision, ((str(row[2])), str(row[1]).lower().capitalize(), str(str(year)+"-"+str(month)+"-"+str(day)), (str(row[0])), (str(files_content[random.randint(0,9)]))))
			conn.commit()
		rg=str(row[2])			

	"""

#df = pd.read_csv('decisions.csv')
#df['count'] = tab_count
#df.to_csv('res_dec.csv', sep=',', index =False)
