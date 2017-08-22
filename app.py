#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, jsonify, json, request
from flaskext.mysql import MySQL
import random, json
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
app.config['MYSQL_CHARSET'] = 'utf-8'
mysql.init_app(app)

conn = mysql.connect()

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

""" Return random color for node/child data"""               
def colors():
    colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"]
    return colores_g[random.randint(0, len(colores_g)-1)]

""" Return a tree with children 'villes' """
@app.route('/get_decisions/')
def get_decisions():
    cur = conn.cursor()
    villes = []
    
    """ Request all cities in database """
    nb = 0
    cur.execute('''SELECT count(*) as nb_ville, ville from decision JOIN demande ON decision.id_decision = demande.id_decision group by ville order by nb_ville desc''')
    data_villes = cur.fetchall()
    for v in data_villes:
        query = "ville = \"" + v[1] + "\""
        d = {'name': v[1], 'nb': v[0], 'tree':'Villes', 'children': [], 'color':colors()}
        villes.append(d)  
        nb += v[0]

    tree_root = {'name':'Filtres', 'nb':nb, 'children':villes, 'color':colors(), "parent": "null"}  
    return jsonify(tree=tree_root)

""" Return children for categorie"""
def categories_links():
    cur = conn.cursor()
    query2 = define_filtres()
    categories = []
    if len(query2) != 0:
        query = '''SELECT count(*) as nb_categorie, objet from decision, demande, categorie WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND
'''+query2+ ''' group by objet order by nb_categorie desc'''
    else:
        query = '''SELECT count(*) as nb_categorie, objet from decision, demande, categorie WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie 
 group by objet order by nb_categorie desc'''
    cur.execute(query)
    categorieParVille = cur.fetchall()
    for c in categorieParVille:
        r = {'name': c[1], 'nb': c[0], 'tree':'Categories', '_children': [], 'color':colors()}
        categories.append(r)
    return categories        

@app.route('/get_categorie/')
def get_categorie():
    categories = categories_links()
    return jsonify(tree=categories)

""" Return children for normes"""            
@app.route('/get_norme/')
def get_norme():
    cur = conn.cursor()
    query2 = define_filtres()
    normes = []
    objet = json.loads(request.args.get('objet')) 
    if len(query2) != 0:
        query2 += " AND objet=\"" + objet +"\" group by norme order by nb_res desc"
    else:
        query2 += " objet=\"" + objet +"\" group by norme order by nb_res desc"
        
    query = '''SELECT count(*) as nb_res, norme from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query2+''
    cur.execute(query)
    normeParVille = cur.fetchall()
    for n in normeParVille:
        r = {'name': n[1], 'nb': n[0], '_children': [], 'tree':'Normes', 'color':colors()}
        normes.append(r)
    return jsonify(tree=normes)

""" Return children for resultats"""  
@app.route('/get_resultat/')
def get_resultat():
    cur = conn.cursor()
    query2 = define_filtres()
    objet = json.loads(request.args.get('objet'))
    norme = json.loads(request.args.get('norme'))

    if len(query2) != 0:
        query2 += " AND objet=\"" + objet +"\" AND norme=\""+norme+"\" group by resultat order by nb_res desc"
    else:
        query2 += " objet=\"" + objet +"\" AND norme=\""+norme+"\" group by resultat order by nb_res desc"
    queryResultats = '''SELECT  count(*) as nb_res, resultat from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query2+''
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
            color = 'yellow'
        d = {'name': r[1], 'nb': r[0], 'tree':'Resultats', 'color':color}
        resParNormeChildren.append(d)
    return jsonify(tree=resParNormeChildren)

@app.route('/sortByVille/')
def sortByVille():
    cur = conn.cursor()
    villes = []
    query2 = define_filtres()
    nb = 0
    """ Request all cities in database """
    if len(query2) != 0:
        query = '''SELECT count(*) as nb_ville, ville from decision JOIN demande ON decision.id_decision = demande.id_decision WHERE ''' + query2 + ' group by ville order by nb_ville desc'
    else:
        query = '''SELECT count(*) as nb_ville, ville from decision JOIN demande ON decision.id_decision = demande.id_decision group by ville order by nb_ville desc'''
    cur.execute(query)
    data_villes = cur.fetchall()
    for v in data_villes:
        query = "ville = \"" + v[1] + "\""
        d = {'name': v[1], 'nb': v[0], 'tree':'Villes', 'children': [], 'color':colors()}
        villes.append(d)  
        nb += v[0]
    tree_root = {'name':'Filtres', 'nb':nb, 'children':villes, 'color':colors(), "parent": "null"}  
    return jsonify(tree=tree_root)

""" Render template index.html"""
@app.route('/')
def index():
    cur = conn.cursor()

    cur.execute('''SELECT count(*) as nb_categorie, objet from categorie JOIN demande ON categorie.id_categorie = demande.id_categorie group by objet order by nb_categorie desc''')
    categories = cur.fetchall()

    #cur.execute('''SELECT distinct ville from decision''')
    cur.execute('''SELECT count(*) as nb_ville, ville from decision group by ville''')
    villes = cur.fetchall()

    """ Add min and masx dates to slider/ not used """
    cur.execute('''SELECT max(date_decision) from decision ''')
    date_max = cur.fetchall()
    date_max = str(date_max[0][0])[:4]

    cur.execute('''SELECT min(date_decision) from decision ''')
    date_min = cur.fetchall()
    date_min = str(date_min[0][0])[:4]

    return render_template('index.html', categories = categories, villes = villes)

""" Build a query """
def define_filtres():
    villes = json.loads(request.args.get('villes'))
    date = json.loads(request.args.get('date'))
    #categories = json.loads(request.args.get('categories'))
    #quantumD = json.loads(request.args.get('quantumD'))
    #quantumR = json.loads(request.args.get('quantumR'))
    #resultat = json.loads(request.args.get('resultat'))
    #juridiction = json.loads(request.args.get('juridiction'))
    texte = json.loads(request.args.get('texte'))
    search = {'date':len(date), 'texte':len(texte), 'villes':len(villes)}
    filters = []

    for key, value in search.iteritems():
        if value > 0:
            filters.append(key)
    
    query2 = ''
        
    for f in filters:
        if f == 'villes':
            liste_villes = ''
            for v in villes[:-1]:
                liste_villes +=" \""+ v + "\", "
            liste_villes += " \""+ villes[-1] + "\""
            if filters[-1] == 'villes':
                query2 += "ville IN ( " + liste_villes + " ) "
            else:
                query2 += "ville IN ( " + liste_villes + " ) AND " 
        
        if f == 'date':
            print date
            if len(date) == 2:
                date1 = str(date[0]) + "-01-01"
                date2 = str(date[1]) + "-01-01"
           
                if filters[-1] == 'date':
                    query2 += "( date_decision BETWEEN '" + date1 + "' AND '" + date2 + "' )"
                else:
                    query2 += "( date_decision BETWEEN '" + date1 + "' AND '" + date2 + "' ) AND "
            else:
                date1 = str(date[0]) + "-01-01"
                date2 = str(date[0]) + "-12-31"               
                if filters[-1] == 'date':
                    query2 += "( date_decision BETWEEN '" + date1 + "' AND '" + date2 + "' )"
                else:
                    query2 += "( date_decision BETWEEN '" + date1 + "' AND '" + date2 + "' ) AND "
                
        if f == 'texte':
            keyWords = texte.split(" ")
            paramToSearch = ''
            #print keyWords
            for w in keyWords:
                if w == "AND" or w == "NOT" or w == "OR":
                    paramToSearch += w + " "
                elif w[-1] == ")":
                    nw = w[:-1]
                    paramToSearch += nw + "~) "
                else:   
                    paramToSearch += w + "~ "
            res = es.search(index = 'index_decision', body = {"query": {"query_string" : {"query": paramToSearch, "fuzziness" : 1, "default_field": "contenu"}}, "size": 470})
            #print('%d documents found' % res['hits']['total'])
            liste_id = []
            for doc in res['hits']['hits']:
                liste_id.append(int(doc['_id']))
            liste_ids = str(liste_id)[1:-1]
            if res['hits']['total'] != 0:
                if filters[-1] == 'texte':
                    query2 += "decision.id_decision IN ( " + liste_ids + " ) "
                else:
                    query2 += "decision.id_decision IN ( " + liste_ids + " ) AND " 
            else:        
                if filters[-1] == 'texte':
                    query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE))"
                else:
                    query2+="( MATCH(description) AGAINST(\""+texte+"\" IN BOOLEAN MODE)) AND " 
            

        """
        if f == 'categories':
            query2 += "("
            for c in categories[:-1]:
                query2 += "categorie=\""+c+ "\" OR "
            if filters[-1] != 'categories':
                query2 += "categorie=\"" + categories[-1] + "\" AND "
            else:
                query2 += "categorie=\"" + categories[-1] + "\")"

        if f == 'resultat':
            query2 += "("
            for r in resultat[:-1]:
                query2 += "resultat=\"" + r + "\" OR "
            if filters[-1] != 'resultat':
                query2 += "resultat=\"" + resultat[-1] + "\") AND "
            else:
                query2 += "resultat=\"" + resultat[-1] + "\")"
        """    
    return query2       

""" Request for show tabel of search results, return first 15 records and available number of pages """
@app.route('/show_text/')
def show_text():
    query2 = define_filtres()
    query = ''
    queryNB = ''

    if len(query2) != 0:
        query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query2+' LIMIT 0, 15 '
        queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme  AND '''+query2
    else:
        query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme LIMIT 0, 15'''
        queryNB = '''SELECT count(*) from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme'''
    
    cur = conn.cursor()
    cur.execute(queryNB)
    nbDem = cur.fetchall()
    nbDemande = nbDem[0][0]
    nbPage = (nbDemande/15) + 1
    cur.execute(query)
    data = cur.fetchall()
    return jsonify(result=data, nbPage=nbPage)
    
""" Return 15 records of requested page """
@app.route('/show_page/')
def show_page():
    numPage = json.loads(request.args.get('numPage')) 
    query2 = define_filtres()
    query = ''
    queryNB = ''
    if len(query2) != 0:
        query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query2+' LIMIT '''+ str(int(numPage)*15) +', 15'
    else:
        query = '''SELECT * from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme LIMIT '''+ str(int(numPage)*15) +", 15"
    
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return jsonify(result=data)


@app.route('/sortByCategorie/')
def get_results():
    categories = categories_links()
    nb = 0
    for c in categories:
    	nb += c.get('nb')
    tree_root = {'name':'Filtres', 'nb':nb, 'children':categories, 'color':colors(), "parent": "null"}
    return jsonify(tree=tree_root)

""" Return results of query grouped by cities """
@app.route('/groupVille/')
def get_group():
    groups = json.loads(request.args.get('groups'))
    cur = conn.cursor()
    children = []
    nbTotal = 0
    for g in groups:
        villes = g.split(",")
        liste_villes = ""
        for v in villes[:-1]:
            liste_villes +=" \""+ v + "\", "
        liste_villes += " \""+ villes[-1] + "\""
        query2 = define_filtres()

        if len(query2) != 0:
            query2 += " AND ville IN ( " + liste_villes + " ) "
        else:
            query2 = " ville IN ( " + liste_villes + " ) "
                
        query = '''SELECT count(*) as nb_ville from decision JOIN demande ON decision.id_decision = demande.id_decision WHERE ''' + query2 
        #print query
        cur.execute(query)
        data_villes = cur.fetchall()
        #print data_villes
        nb = data_villes[0][0]
        if nb != 0:
       		d = {'name': villes, 'nb': nb, 'tree':'Villes', 'children': [], 'color':colors()}
        	children.append(d)
        	nbTotal += nb

    tree_root = {'name':'Filtres', 'nb':nbTotal, 'children':children, 'color':colors(), "parent": "null"}
    return jsonify(tree=tree_root)

""" Return quantum_demande, quantum_demande, date to build an histigram """
@app.route('/get_quantum/')
def get_quantum():
    norme = json.loads(request.args.get('objet'))    
    objet = json.loads(request.args.get('norme'))    
    resultat = json.loads(request.args.get('resultat')) 
    query2 = define_filtres()
    if len(query2) > 0:
         query2+=" AND "
    query2 += " norme = \"" + norme + "\" AND objet = \"" + objet  + "\" AND resultat = \"" + resultat + "\" ORDER BY date_decision "
    cur = conn.cursor()
    query = '''SELECT quantum_demande, quantum_resultat, date_decision, resultat from decision, demande, categorie, norme WHERE decision.id_decision = demande.id_decision AND categorie.id_categorie = demande.id_categorie AND demande.id_norme = norme.id_norme AND '''+query2
    cur.execute(query)
    quantums = cur.fetchall()
    all_quantums = []
   
    for q in quantums:
        if str(q[2])!='None':
            d = {'quantum_demande':q[0],'quantum_resultat': q[1], 'date': q[2], 'resultat':q[3] }
            all_quantums.append(d)
           
    return jsonify(quantums=all_quantums)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
