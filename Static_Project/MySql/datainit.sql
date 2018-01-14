drop database if exists kkidb;
CREATE DATABASE IF NOT EXISTS kkidb;
use kkidb;

SET FOREIGN_KEY_CHECKS=0; /* don't do this, it isn't smart. just lazy coding */
/***************** PEOPLE part (part 1) ******************/
create table if not exists catdb_cat_owners(
    id int AUTO_INCREMENT NOT NULL primary key,
    cat_id int,
    owner_id int,
    foreign key(cat_id) references catdb_cat(id) ON DELETE CASCADE,
    foreign key(owner_id) references catdb_people(id) ON DELETE CASCADE,
    regdate date
);

create table if not exists catdb_people(
    id int AUTO_INCREMENT primary key,
    name varchar(50) not null,
    id_num varchar(30) not null,
	ssn char(10),
    address varchar(40),
    postal char(3),
    phone char(10),
    email varchar(30),
    member_id int,
    comment varchar(144)
);

create table if not exists Cateries(
	id int auto_increment primary key,
	name varchar(50),
	prefix boolean,
	national boolean,
	country varchar(3)
);

/***************** CAT part (part 2)  *************/

create table if not exists catdb_cat(
    id int AUTO_INCREMENT not null primary key,
    reg_nr varchar(5),
    name varchar(35) not null,
    gender bool not null,
    birth date,
    registered date,
    dam_id int,
    sire_id int,
    foreign key(dam_id) references catdb_parents(id) ON DELETE CASCADE,
    foreign key(sire_id) references catdb_parents(id) ON DELETE CASCADE,
    comments varchar(144),
    type varchar(3)
);

create table if not exists catdb_ghost_cat(
    id int AUTO_INCREMENT not null primary key,
    reg_nr varchar(30),
    name varchar(50),
    birth date,
    microchip varchar(30),
    dam_id int,
    sire_id int,
    foreign key(dam_id) references catdb_parents(id) ON DELETE CASCADE,
    foreign key(sire_id) references catdb_parents(id) ON DELETE CASCADE
);

create table if not exists catdb_parents(
    id int AUTO_INCREMENT primary key,
    is_ghost boolean not null,
    cat_id int,
    ghost_id int,
    foreign key(cat_id) references catdb_cat(id) ON DELETE CASCADE,
    foreign key(ghost_id) references catdb_ghost_cat(id) ON DELETE CASCADE
);

create table if not exists catdb_imp_cat(
    id int AUTO_INCREMENT NOT NULL primary key,
    cat_id int NOT NULL,
    foreign key(cat_id) references catdb_cat(id) ON DELETE CASCADE,
    org_country varchar(3),
    org_organization varchar(10),
    org_reg_nr varchar(20),
    attachment blob
);


create table if not exists catdb_cat_EMS(
    id int AUTO_INCREMENT NOT NULL primary key,
    cat_id int,
    ems_id int,
    foreign key(cat_id) references catdb_cat(id) ON DELETE CASCADE,
    foreign key(ems_id) references catdb_EMS(id) ON DELETE CASCADE,
    reg_date date not null
);

create table if not exists catdb_ghost_EMS(
    id int AUTO_INCREMENT NOT NULL primary key,
    ghost_id int,
    ems_id int,
    foreign key(ghost_id) references catdb_ghost_cat(id) ON DELETE CASCADE,
    foreign key(ems_id) references catdb_EMS(id) ON DELETE CASCADE
);

create table if not exists catdb_EMS(
    id int AUTO_INCREMENT NOT NULL primary key,
    breed varchar(3),
    ems_key varchar(15)
);

create table if not exists catdb_neutered(
    id int AUTO_INCREMENT NOT NULL primary key,
    cat_id int not null,
    date date not null,
    foreign key(cat_id) references catdb_cat(id) ON DELETE CASCADE
);

create table if not exists catdb_microchip(
    id int AUTO_INCREMENT NOT NULL primary key,
    cat_id int not null,
    microchip_nr varchar(30) not null UNIQUE,
    foreign key(cat_id) references catdb_cat(id)
);

create table if not exists catdb_group(
    id int AUTO_INCREMENT NOT NULL primary key,
    breed varchar(50),
    ems varchar(50),
    groupp varchar(50)
);

create table if not exists catdb_category(
    id int AUTO_INCREMENT NOT NULL primary key,
    breed varchar(50),
    category varchar(50)
);

/***************** JUDGE/SHOW part (part 3)  *************/
create table if not exists catdb_show(
	id int AUTO_INCREMENT Primary key,
	show_name varchar(50) not null,
	date date not null,
	show_orginizer varchar(50)
);

create table if not exists catdb_show_entry(
	showId int not null,
	catId int not null, 
	show_nr int not null
);

alter table catdb_show_entry
add primary key(showId,catId);

alter table catdb_show_entry
add foreign key(catId) references catdb_cat(id) ON DELETE CASCADE;

alter table catdb_show_entry
add foreign key(showId) references catdb_show(id) ON DELETE CASCADE;

create table if not exists catdb_judge(
	id int AUTO_INCREMENT primary key,
	cat1 boolean,
	cat2 boolean,
	cat3 boolean,
	cat4 boolean,
	cat5 boolean
);

create table if not exists catdb_cert(
	id int AUTO_INCREMENT primary key,
	title varchar(50),
	req_cert integer
);

create table if not exists catdb_judgement(
	id int AUTO_INCREMENT Primary Key, 
	cat int not null, 
	showId int not null, 
	judge int not null, 
	certId int, 
	attendence boolean, 
	ex int, 
	cert boolean, 
	biv boolean, 
	nom boolean, 
	litter boolean, 
	color boolean, 
	comment varchar(2048), 
	show_nr int 
);

alter table catdb_judgement
add foreign key(cat) references catdb_cat(id) ON DELETE CASCADE;

alter table catdb_judgement
add foreign key(showId) references catdb_show(id) ON DELETE CASCADE;

alter table catdb_judgement
add foreign key(judge) references catdb_show(id) ON DELETE CASCADE;


SET FOREIGN_KEY_CHECKS = 1;