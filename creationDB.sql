drop table demande;
drop table decision;

#create database decisionsJustice; 

create table decision ( 
	id_decision INT(10) NOT NULL AUTO_INCREMENT,
	rg VARCHAR(10),
	ville VARCHAR(15),
	juridiction VARCHAR(20),
	description VARCHAR(2000), 
	primary key (id_decision)
) ;

create table demande ( 
	id_decision INT(10) NOT NULL, 
	quantum_demande VARCHAR(20),
	quantum_resultat VARCHAR(20),
	categorie  VARCHAR(100),
	resultat ENUM('accepte','rejette', 'irrecevable', 'sursis à statuer'),
	primary key (id_decision),
	constraint fk_decision foreign key (id_decision) references decision(id_decision)

);

#insert into decision(rg, ville, juridiction, description) values ("10/03813", "Nimes", "CA","description");
#insert into demande(id_decision, quantum_demande, quantum_resultat, categorie, resultat) values (1, "1684,32 €","1684,32 €", "dommages-intérêts","accepte");

#select decision.id_decision, decision.rg, decision.ville, decision.juridiction, decision.description, demande.quantum_demande, demande.categorie
#from decision join demande on decision.id_decision = demande.id_decision;