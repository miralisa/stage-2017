drop table demande;
drop table decision;
drop table categorie;
drop table norme;
#create database decisionsJustice; 

create table norme ( 
	id_norme INT(10) NOT NULL AUTO_INCREMENT,
	norme  VARCHAR(100),
	primary key (id_norme)
);

create table categorie ( 
	id_categorie INT(10) NOT NULL AUTO_INCREMENT, 
	objet  VARCHAR(100),
	primary key (id_categorie)
);

create table decision ( 
	id_decision INT(10) NOT NULL AUTO_INCREMENT,
	rg VARCHAR(10),
	ville VARCHAR(15),
	date_decision DATE,
	juridiction VARCHAR(20),
	description text, 
	primary key (id_decision)
);

ALTER TABLE decision ADD FULLTEXT(description);


create table demande ( 
	id_demande INT(10) NOT NULL AUTO_INCREMENT, 
	quantum_demande VARCHAR(20),
	quantum_resultat VARCHAR(20),
	resultat ENUM('accepte','rejette', 'sursis à statuer'),#, 'irrecevable'
	id_decision INT(10),
	id_categorie INT(10),
	id_norme INT(10),
	primary key (id_demande),
	constraint fk_demande_decision foreign key (id_decision) references decision(id_decision),
	constraint fk_demande_categorie foreign key (id_categorie) references categorie(id_categorie),
	constraint fk_demande_norme foreign key (id_norme) references norme(id_norme)


);

#insert into decision(rg, ville, juridiction, description) values ("10/03813", "Nimes", "CA","description");
#insert into demande(id_decision, quantum_demande, quantum_resultat, categorie, resultat) values (1, "1684,32 €","1684,32 €", "dommages-intérêts","accepte");

#select decision.id_decision, decision.rg, decision.ville, decision.juridiction, decision.description, demande.quantum_demande, demande.categorie
#from decision join demande on decision.id_decision = demande.id_decision;

#SELECT count(*) as nb_categorie, objet from categorie JOIN demande ON categorie.id_categorie = demande.id_categorie group by objet order by nb_categorie desc ;


