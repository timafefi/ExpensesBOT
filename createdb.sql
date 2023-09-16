create table usr(
    id integer primary key,
	userid integer,
    first_name integer,
    last_name integer,
    is_bot boolean,
    username varchar (255),
    admin boolean default False,
    blacklist boolean default False
);

create table expences(
	id integer primary key,
	_type boolean,
	usr_id integer,
	amount float,
	msg varchar(255),
	category integer default -1,
	created_dt float,
	FOREIGN KEY (usr_id) REFERENCES usr(userid)
);


create table earn_sum(
	userid integer primary key,
	amount float default 0,
	FOREIGN KEY (userid) REFERENCES USR(USERID)
);


create table spend_sum(
	userid integer primary key,
	amount float,
	FOREIGN KEY (userid) REFERENCES USR(USERID)
);
