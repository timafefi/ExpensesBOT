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
	userid integer,
	amount float,
	msg varchar(255),
	category integer default -1,
	created_dt float,
	FOREIGN KEY (userid) REFERENCES usr(userid)
);
