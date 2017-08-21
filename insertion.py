# -*-coding:Latin-1 -*

from flask import Flask, render_template
from flaskext.mysql import MySQL
import csv, random, json
import os

app = Flask(__name__)
mysql = MySQL()

file_ids = open("database_identifiers.json", "r")
ids = json.load(file_ids)
file_ids.close()

app.config['SECRET_KEY'] = 'secret!'
app.config['MYSQL_DATABASE_USER'] = str(ids['login'])
app.config['MYSQL_DATABASE_PASSWORD'] = str(ids['password'])
app.config['MYSQL_DATABASE_DB'] = str(ids['database_name'])
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
""" Queries for insert data into different tables """
insDecision = """INSERT INTO decision (rg, ville, date_decision, juridiction, description) values (%s,%s,%s,%s,%s)"""
insDemande = """INSERT INTO  demande (quantum_demande, quantum_resultat, id_categorie, id_norme, resultat, id_decision) values (%s,%s,%s,%s,%s,%s)"""
insCategorie = """INSERT INTO categorie (objet) values (%s) """
insNorme = """INSERT INTO norme (norme) values (%s) """

cur=conn.cursor()
file = open("decisions.csv", "rb")
cr = csv.reader(file)

""" Create dict files_content with ref and text of decisions """
files_content = {}

path = os.path.abspath(".") + "/dataset-renamed/"

for row in cr:
	villeDec = str(row[1]).upper()
	if str(row[1])=="Nîmes":
		villeDec = "NIM"
	rgDec = str(row[2])
	rgDecF = rgDec.split("/")
	ref = ''
	for l in rgDecF:
		ref += l
	
	for filename in os.listdir(path):
		fileVille = filename[2:5]
		rg = filename[5:12]

		if str(row[15])!="0" and fileVille==villeDec[0:3] and ref==rg:
			f = open(path + filename, "rb")
			files_content.update({str(ref) : f.read()})

""" Point to first line of file """		
file.seek(0)
next(cr)


count = 0
tab_count = []
next(cr)
rg = ''
objets = []
normes = []
dictNormes = {}
dictCat = {}

for row in cr:
	# insert into table 'norme'
	if str(row[15])!="0" and (str(row[5]) not in normes):
		count +=1
		cur.execute(insNorme, (str(row[5])))
		conn.commit()
		normes.append(str(row[5]))
		dictNormes.update({str(row[5]): count })

file.seek(0)
next(cr)
count = 0
for row in cr:
	# insert into table 'categorie'
	if str(row[15]) != "0" and (str(row[3]) not in objets):
		cur.execute(insCategorie, (str(row[3]))) #id_norme =  dictNormes.get(str(row[5]))
		conn.commit()
		objets.append(str(row[3]))
		count += 1
		dictCat.update({str(row[3]): count})


file.seek(0)
next(cr)

count = 0
for row in cr:	
	# Insert into table 'decision'
	if (str(row[3])=="x" or str(row[3])==" " or str(row[3])=="" or str(row[3])=="Faux positif DI" or str(row[3])=="error" or str(row[11])=="" or str(row[11])==" " or str(row[11])=="  " or str(row[11])=="irrecevable" ):
		tab_count.append(0)
	else:
		
		if str(row[2])==rg:
			tab_count.append(count)
			
		else:
			count += 1
			tab_count.append(count)
			
			""" generate random date """
			year = random.randint(2000, 2017)
			day = random.randint(1, 30)
			month = random.randint(1, 12)

			rgDec = str(row[2])
			rgDecF = rgDec.split("/")
			ref = ''
		
			for l in rgDecF:
				ref += l
			getText = files_content.get(ref, "None")

			cur.execute(insDecision, ((str(row[2])), str(row[1]).lower().capitalize(), str(str(year)+"-"+str(month)+"-"+str(day)), (str(row[0])), getText))
			conn.commit()
		rg = str(row[2])			

file.seek(0)
next(cr)

for row in cr:	
	# insert into table 'demande'
	if str(row[15])!="0":
		cur.execute(insDemande, ((str(row[7])),(str(row[13])), dictCat.get(str(row[3])), dictNormes.get(str(row[5])), (str(row[11])), (str(row[15]))))
		conn.commit()	
	
