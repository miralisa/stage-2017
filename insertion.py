# -*-coding:Latin-1 -*

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
insDemande = """INSERT INTO  demande (quantum_demande, quantum_resultat, id_categorie, id_norme, resultat, id_decision) values (%s,%s,%s,%s,%s,%s)"""
insCategorie = """INSERT INTO categorie (objet) values (%s) """
insNorme = """INSERT INTO norme (norme) values (%s) """

cur=conn.cursor()
file = open("res_dec.csv","rb")
cr = csv.reader(file)
#writer = csv.writer(open('output.csv', 'w'))

# Open text files of decisions to put content in field 'description'
"""
files_content = []
for filename in os.listdir("/home/anastasiia/Documents/stage-2017/dataset-renamed"):
	if filename
	f = open("/home/anastasiia/Documents/stage-2017/decision-de-justice/"+filename, "rb")
	files_content.append(f.read())
	#print files_content
"""
files_content = {}

for row in cr:
	villeDec = str(row[1]).upper()
	if str(row[1])=="Nîmes":
		villeDec = "NIM"
	rgDec = str(row[2])
	#print villeDec[0:3]
	rgDecF = rgDec.split("/")
	ref = ''
	for l in rgDecF:
		ref +=l
	
	for filename in os.listdir("/home/anastasiia/Documents/stage-2017/dataset-renamed"):
		#if filename[2:4]
		fileVille = filename[2:5]
		rg = filename[5:12]

		if str(row[15])!="0" and fileVille==villeDec[0:3] and ref==rg:
			#print ref
			f = open("/home/anastasiia/Documents/stage-2017/dataset-renamed/"+filename, "rb")
			files_content.update({str(ref) : f.read()})

	
#print files_content["1005370"];
file.seek(0)
next(cr)

"""
for row in cr:
	if str(row[15])!="0":
		for filename in os.listdir("/home/anastasiia/Documents/stage-2017/dataset-renamed"):
			#if filename[2:4]
			print filename[2:4]
			print filename[4:6]

		#(str(row[2]))
		#str(row[1]).lower().capitalize()
"""	



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
	if str(row[15])!="0" and (str(row[3]) not in objets):
		cur.execute(insCategorie, (str(row[3]))) #id_norme =  dictNormes.get(str(row[5]))
		conn.commit()
		objets.append(str(row[3]))
		count +=1
		dictCat.update({str(row[3]): count})


file.seek(0)
next(cr)

count = 0
for row in cr:	
	# Insert into table 'decision'
	if (str(row[3])=="x" or str(row[3])==" " or str(row[3])=="" or str(row[3])=="Faux positif DI" or str(row[3])=="error" or str(row[11])=="" or str(row[11])==" " or str(row[11])=="  " or str(row[11])=="irrecevable" ):
		#if (str(row[7]))!="-" or (str(row[7]))!="?" or (str(row[13]))!="-" or (str(row[13]))!="?":
		tab_count.append(0)
		#print str(row[1]).lower().capitalize()
	else:
		#print row[15]
		
		if str(row[2])==rg:
			#print rg
			tab_count.append(count)
			#cur.execute(insDemande, ((str(row[7])),(str(row[13])),(str(row[3])),(str(row[11])), count))			
			#conn.commit()
			
		else:
			count+=1
			tab_count.append(count)
			year = random.randint(2000,2017)
			day = random.randint(1,30)
			month = random.randint(1,12)

			rgDec = str(row[2])
			#print villeDec[0:3]
			rgDecF = rgDec.split("/")
			ref = ''
			for l in rgDecF:
				ref +=l
			
			#print ref	
			getText = files_content.get(ref, "None")
			#print getText
			cur.execute(insDecision, ((str(row[2])), str(row[1]).lower().capitalize(), str(str(year)+"-"+str(month)+"-"+str(day)), (str(row[0])), getText))
			conn.commit()
		rg=str(row[2])			

file.seek(0)
next(cr)

print dictCat
print dictNormes	

for row in cr:	
	# insert into table 'demande'
	if str(row[15])!="0":
		#print dictCat.get(str(row[3]))
		#print str(row[3])
		#print dictNormes.get(str(row[5]))
		#print str(row[5])
	
		cur.execute(insDemande, ((str(row[7])),(str(row[13])), dictCat.get(str(row[3])), dictNormes.get(str(row[5])), (str(row[11])), (str(row[15]))))
		conn.commit()	
	

#print dictNormes[0]['id']

#df = pd.read_csv('decisions.csv')
#df['count'] = tab_count
#df.to_csv('res_dec.csv', sep=',', index =False)