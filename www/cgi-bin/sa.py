#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import json
import MySQLdb as mysql

fields = ["name", "email", "datafile"]
path = "/home/deck/work/sa/sa-web/sources/"


def addRecord(name, email, path):
	db = mysql.connect(host='poddy.org', user='saweb', passwd='passSaWeb')
	handler = db.cursor()
	handler.execute('use saweb')

	handler.execute("SELECT id FROM users WHERE email = '%s'" % (email,))
	results = handler.fetchall()
	if len(results) == 0:
		handler.execute("INSERT into users (name, email) VALUES('%s', '%s')" % (name, email))
		db.commit()
		handler.execute("INSERT into requests (user_id, source_path) VALUES(LAST_INSERT_ID(), '%s')" % (path,))
		db.commit()

	user_id = results[0][0]
	handler.execute("INSERT into requests (user_id, source_path) VALUES(%s, '%s')" % (user_id, path))
	db.commit()
	db.close()




def  checkForm(form):
	for field in fields:
		if field not in form:
			return False
	return True

def processForm(form):
	name = form["name"].value
	email = form["email"].value
	filename = "%s/%s_%s_%s" % (path, name, email, form["datafile"].filename)
	fh = open(filename, "wb")
	fh.write(form["datafile"].file.read())
	fh.close();
	addRecord(name, email, filename)
	return True

def sendAnswer(success):
	dct = {"success": success}
	dct["msg"] = ("Failure", "Okay")[success]
	print json.dumps(dct)
	exit()

def main():
	form = cgi.FieldStorage()
	print "Content-type: application/json\n"

	if not checkForm(form):
		sendAnswer(False)

	res = processForm(form)
	sendAnswer(res)
	 

main()