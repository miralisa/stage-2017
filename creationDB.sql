#create database decisionsJustice; 

DROP INDEX iville ON decision;
DROP INDEX inorme ON norme;
DROP INDEX iobjet ON categorie;

drop table demande;
drop table decision;
drop table categorie;
drop table norme;

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
	resultat ENUM('accepte','rejette', 'sursis à statuer'),
	id_decision INT(10),
	id_categorie INT(10),
	id_norme INT(10),
	primary key (id_demande),
	constraint fk_demande_decision foreign key (id_decision) references decision(id_decision),
	constraint fk_demande_categorie foreign key (id_categorie) references categorie(id_categorie),
	constraint fk_demande_norme foreign key (id_norme) references norme(id_norme)


);

CREATE INDEX iville ON decision (ville);
CREATE INDEX inorme ON norme (norme);
CREATE INDEX iobjet ON categorie (objet);
