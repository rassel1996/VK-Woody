#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3

db     = sqlite3.connect('db')
cursor = db.cursor()

def getAssoc(names):
	cursor.execute('''SELECT %s FROM app''' % (names))
	columns      = cursor.fetchone()
	columnsNames = names.replace(" ", "").split(",")

	elements = {}

	for key, column in enumerate(columns):
		elements[columnsNames[key]] = column

	db.commit()

	return elements


def getOne(name):
	cursor.execute('''SELECT %s FROM app''' % (name))
	return cursor.fetchone()[0]
	db.commit()


def update(set):
	cursor.execute('''UPDATE app SET %s''' % (set))
	db.commit()



# cursor.execute('''CREATE TABLE app(token TEXT, user_id TEXT, email TEXT unique, password TEXT)''')
# cursor.execute('''INSERT INTO app(token, user_id, email, password) VALUES(?,?,?,?)''', ("token", "user_id", "email", "password"))
# db.getOne("token") # result
# db.getAssoc("token, user_id") # assoc
# db.insert('token, user_id, email, password', 'token, user_id, email, password')
# db.update("token")