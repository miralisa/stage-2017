### Prerequies

* (X/L/_)Ubuntu LTS x86_64 >= 14.04.5
* MySql 14.14
* Python 2.7.x
* Python libraries: Flask, elasticsearch, Flask-mysql

### Install Python libraries using pip

	pip install flask
	pip install flask-mysql
	pip install elasticsearch

### Configure and create a database

Create a database with the name of your choice

Specify a login, a password and a database name in database_identifiers.json

### Connect to your database
	
To create the tables needed, do:

		source creationDB.sql

### Insert new records into a database

To insert data, use the commande below:

		python insertion.py

### Install and configure elasticsearch
	
To install elasticsearch follow step 1, 2 of this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-14-04)
		
	
To create elasticsearch index and put data to ES server, do:

		python indexES.py

Launch ES server:

		sudo service elasticsearch start 

### Execution

To start the server, do:

		python app.py

To display a site, open a web browser and type in the adress bar:

		http://127.0.0.1:5000/

### Ending

You can shut down the server by typing CTRL+C


