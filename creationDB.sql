drop table demande;
drop table decision;

#create database decisionsJustice; 

create table decision ( 
	id_decision INT(10) NOT NULL AUTO_INCREMENT,
	rg VARCHAR(10),
	ville VARCHAR(15),
	date_decision DATE,
	juridiction VARCHAR(20),
	description text, 
	primary key (id_decision)
) ;

ALTER TABLE decision ADD FULLTEXT(description);

create table demande ( 
	id_demande INT(10) NOT NULL AUTO_INCREMENT, 
	quantum_demande VARCHAR(20),
	quantum_resultat VARCHAR(20),
	categorie  VARCHAR(100),
	resultat ENUM('accepte','rejette', 'sursis à statuer'),#, 'irrecevable'
	id_decision INT(10),
	primary key (id_demande),
	constraint fk_demande_decision foreign key (id_decision) references decision(id_decision)

);

#insert into decision(rg, ville, juridiction, description) values ("10/03813", "Nimes", "CA","description");
#insert into demande(id_decision, quantum_demande, quantum_resultat, categorie, resultat) values (1, "1684,32 €","1684,32 €", "dommages-intérêts","accepte");

#select decision.id_decision, decision.rg, decision.ville, decision.juridiction, decision.description, demande.quantum_demande, demande.categorie
#from decision join demande on decision.id_decision = demande.id_decision;
