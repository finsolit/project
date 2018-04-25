# -*- coding: utf-8 -*-
import telebot
import pickle
import sqlite3
import datetime
from telebot import types

conn = sqlite3.connect('test2.db')
c = conn.cursor()

def add_reserv(u_id_user, u_name, u_number, u_num_per, u_time, u_date):
	c.execute("INSERT INTO reservation (id_user,name,number,num_per,time,date) VALUES ('%s','%s','%s','%s','%s','%s')"
	          % (u_id_user, u_name, u_number, u_num_per, u_time, u_date))
	conn.commit()


#Вводим данные
def e_name(message):
	global name
	name = message.text
	msg = send_message(message.chat.id, 'Введите номер:')
	bot.register_next_step_handler(msg, e_number)

def e_number(message):
	global name
	number = message.text
	# Делаем запрос в базу
	id_user = 1
	num_per = 3
	time = 12.00
	date_now = '24.04.2018'
	# print("Список пользователей:\n")
	add_reserv(id_user, name, number, num_per, time, date_now)


'''
id_user = input("Введите id\n")
name = input("Введите имя\n")
number = input("Введите телефон\n")
num_per = input("Введите кол. персон\n")
time = input("Введите время\n")
date_now = datetime.date.today()
print('\n')
#Делаем запрос в базу
id_user = 1
num_per = 3
time = 12.00
date_now = '24.04.2018'
#print("Список пользователей:\n")
add_reserv(id_user,name,number,num_per,time,date_now)
c.execute('SELECT * FROM reservation')
row = c.fetchone()
#выводим список пользователей в цикле
while row is not None:
   print("id:"+str(row[0])+" ID: "+row[1]+" | Имя: "+row[2]+" | Номер: "+row[3]+" | Кол. пер: "+row[4]+" | Время: "+row[5]+" | Дата: "+row[6])
   row = c.fetchone()
'''
# закрываем соединение с базой
c.close()
conn.close()