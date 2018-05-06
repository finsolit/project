# -*- coding: utf-8 -*-
import sqlite3
import time


def add_question(str0):
	question = str0
	conn = sqlite3.connect('module.db')
	cur = conn.cursor()
	try:
		cur.execute("INSERT INTO table1 (question) VALUES ('%s')" % (question))
		conn.commit()
		cur.execute("SELECT * FROM table1 ORDER BY id DESC LIMIT 1")
		row = cur.fetchone()
		return True
	except:
		return False
	cur.close()
	conn.close()

def ask_question():
	t_1_q = []
	conn = sqlite3.connect('module.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM table1")
	rows = cur.fetchall()
	for i in range(0,len(rows)):
		#bot.bot.send_message(message.chat.id, 'id: '+str(row[0]) + ' question: '+str(row[1]))
		t_1_q.append(str(rows[i][1]))
	return t_1_q
	conn.commit()
	cur.close()
	conn.close()

def del_question(message):
	del_str = message
	conn = sqlite3.connect('module.db')
	cur = conn.cursor()
	try:
		cur.execute("DELETE FROM table1 where question = '%s'" % del_str)
		conn.commit()
		return True
	except:
		return False
	cur.close()
	conn.close()

def bid_response(str1,str2):
	date =  str(int(time.time()))
	conn = sqlite3.connect('module.db')
	cur = conn.cursor()
	try:
		cur.execute("INSERT INTO table2 (question1, question2, date) VALUES ('%s','%s','%s')" % (str1,str2,date))
		conn.commit()
		return True
	except:
		return False
	cur.close()
	conn.close()

def ask_response(time):
	t_2_q1 = []
	t_2_q2 = []
	conn = sqlite3.connect('module.db')
	cur = conn.cursor()
	cur.execute('SELECT * FROM table2')
	rows = cur.fetchall()

	for row in rows:
		if int(row[3]) > time:
			t_2_q1.append(row[1])
			t_2_q2.append(row[2])
	return t_2_q1,t_2_q2

	cur.close()
	conn.close
