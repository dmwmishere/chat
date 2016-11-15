import sqlite3


def makeStructure(where):
    db = sqlite3.connect(where)
    c = db.cursor()
    c.execute(
        '''
	create table users(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	login varchar(64) unique not null,
	pswd varchar(36),
	name varchar(64),
	state INTEGER,
	last_login timestamp
	)''')
    c.execute(
        '''
	create table chats(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	topic varchar(255)
	)''')
    c.execute(
        '''
	create table usersinchats(
	userid INTEGER not null,
	chatid INTEGER not null,
	primary key(userid, chatid)
	)''')
    c.execute(
        '''
	create table messages(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	chatid INTEGER not null,
	userid INTEGER not null,
	message varchar(1024),
	priority INTEGER
	)''')
    db.commit()
    db.close()
