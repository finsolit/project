# -*- coding: utf-8 -*-
import telebot
import re
import requests
import os
import urllib
import sqlite3
from telebot import types
import pickle
import datetime
import cherrypy


TOKEN = '550267011:AAHyJ20FhScFC4ckcCW9RDNEyhKbWon3L2s'

WEBHOOK_HOST = '95.46.98.126'
WEBHOOK_PORT = 80  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

#ТУТ БОТ
bot = telebot.TeleBot(TOKEN)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

admin_active = False
admin = []
if os.stat('admin.pkl').st_size > 0:
	file = open('admin.pkl', 'rb')
	admin = pickle.load(file)
	file.close()

inter = []
if os.path.getsize('inter.pkl') > 0:
	file_inter = open('inter.pkl', 'rb')
	inter = pickle.load(file_inter)
	file_inter.close()


kitch = []
if os.path.getsize('kitch.pkl') > 0:
	file_kitch = open('kitch.pkl', 'rb')
	kitch = pickle.load(file_kitch)
	file_kitch.close()

is_active_change = 0                #переменная для хранения нажатия кнопки об замене фото в галереи
num_change = 0

@bot.message_handler(commands=['start', 'help'])
def start(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Меню','Бронь','Галерея','Контанты']])
	msg = bot.send_message(message.chat.id, '<b>Добро пожаловать в Ресторан</b>'+'\n'+'\n'+'Тут вы сможете:'+'\n'+
	'Просмотреть меню'+'\n'+
	'Забронировать столик'+'\n'+
	'Просмотреть Галерею'+'\n'+
	'Просмотреть контактную информацию', parse_mode = 'html',
	reply_markup = keyboard)

@bot.message_handler(commands=['admin'])
def start_admin(message):
	try:
		file = open('admin.pkl', 'rb')
		if os.stat('admin.pkl').st_size == 0:
			msg = bot.send_message(message.chat.id, 'Введите пароль для создания adminpage:')
			bot.register_next_step_handler(msg, new_pass)
		else:
			msg = bot.send_message(message.chat.id, 'Введите пароль:')
			bot.register_next_step_handler(msg, check_pass)
			file.close()
	except IOError as e:
		file = open('admin.pkl', 'wb')
	file.close


def new_pass(message):
	file = open('admin.pkl', 'wb')
	admin.append(message.text)
	admin.append(message.chat.id)
	pickle.dump(admin, file, 2)
	msg = bot.send_message(message.chat.id, 'Теперь у вас есть adminpage!!!!')
	msg = bot.send_message(message.chat.id, '/admin')
	file.close()

def check_pass(message):
	global admin_active
	global admin
	if message.text == admin[0]:
		admin_active = True
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in
					   ['Редак. Гал.', 'Прос. брон.','Выйти']])
		msg = bot.send_message(message.chat.id, 'Добро пожаловать в adminpage', reply_markup=keyboard)
	else:
		msg = bot.send_message(message.chat.id, 'Пароль введен не верно')
	file.close()

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	name(message)


@bot.callback_query_handler(func=lambda c:True)
def inline(c):
	global admin_active
	global  is_active_change
	global inter
	global kitch
	if os.path.getsize('inter.pkl') > 0:
		file_inter = open('inter.pkl', 'rb')
		inter = pickle.load(file_inter)
		file_inter.close()

	if os.path.getsize('kitch.pkl') > 0:
		file_kitch = open('kitch.pkl', 'rb')
		kitch = pickle.load(file_kitch)
		file_kitch.close()

	last_mes = c.message.message_id

	if c.data == 'Назад':
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Меню','Бронь','Галерея','Контанты']])
		msg = bot.send_message(c.message.chat.id, '<b>Добро пожаловать в Ресторан</b>'+'\n'+'\n'+'Тут вы сможете:'+'\n'+
	'Просмотреть меню'+'\n'+
	'Забронировать столик'+'\n'+
	'Просмотреть Галерею'+'\n'+
	'Просмотреть контактную информацию', parse_mode = 'html',
	reply_markup = keyboard)


	if c.data == 'Завтраки':
		msg = bot.send_message(c.message.chat.id, 'Завтраки:')
	if c.data == 'Большой обед':
		msg = bot.send_message(c.message.chat.id, 'Большие обеды:')
	if c.data == 'Основное меню':
		msg = bot.send_message(c.message.chat.id, 'Основное меню:')
	if c.data == 'Барная карта':
		msg = bot.send_message(c.message.chat.id, 'Барная карта:')
	if c.data == 'Винная карта':
		msg = bot.send_message(c.message.chat.id, 'Винная карта:')

	if c.data == 'Интерьер':
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name+'i1') for name in ['⬅', '➡']])
		msg = bot.send_photo(c.message.chat.id, photo=open('galery/interior/1.jpg', 'rb'), reply_markup=keyboard)
	if c.data == 'Кухня':
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name+'k1') for name in ['⬅', '➡']])
		msg = bot.send_photo(c.message.chat.id, photo=open('galery/kitchen/1.jpg', 'rb'), reply_markup=keyboard)

	if c.data[0] == '⬅' and c.data[1] != 'k':
		n=0
		for k in inter:
			if k==c.data[2]:
				n=int(k)-1
		if n==0:
			n=len(inter)
		msg = bot.delete_message(c.message.chat.id, last_mes)
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name+'i'+str(n)) for name in ['⬅', '➡']])
		msg = bot.send_photo(c.message.chat.id, photo=open('galery/interior/'+str(n)+'.jpg', 'rb'),caption='id:'+str(n), reply_markup=keyboard)


	if c.data[0] == '➡' and c.data[1] != 'k':
		n=0
		for k in inter:
			if k==c.data[2]:
				n=int(k)+1
		if n==len(inter)+1:
			n=1
		if n==0:
			n=2
		msg = bot.delete_message(c.message.chat.id, last_mes)
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name+'i'+str(n)) for name in ['⬅', '➡']])
		msg = bot.send_photo(c.message.chat.id, photo=open('galery/interior/'+str(n)+'.jpg', 'rb'),caption='id:'+str(n), reply_markup=keyboard)


	if c.data[0] == '⬅' and c.data[1] == 'k':
		n=0
		for k in kitch:
			if k==c.data[2]:
				n=int(k)-1
		if n==0:
			n=len(kitch)
		msg = bot.delete_message(c.message.chat.id, last_mes)
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name+'k'+str(n)) for name in ['⬅', '➡']])
		msg = bot.send_photo(c.message.chat.id, photo=open('galery/kitchen/'+str(n)+'.jpg', 'rb'), reply_markup=keyboard)


	if c.data[0] == '➡' and c.data[1] == 'k':
		n=0
		for k in kitch:
			if k==c.data[2]:
				n=int(k)+1
		if n==len(kitch)+1:
			n=1
		if n==0:
			n=2
		msg = bot.delete_message(c.message.chat.id, last_mes)
		keyboard = types.InlineKeyboardMarkup(row_width=3)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name+'k'+str(n)) for name in ['⬅', '➡']])
		msg = bot.send_photo(c.message.chat.id, photo=open('galery/kitchen/'+str(n)+'.jpg', 'rb'), reply_markup=keyboard)

	def e_name(message):
		global name
		name = message.text
		msg = bot.send_message(message.chat.id, 'Введите номер телефона:')
		bot.register_next_step_handler(msg, e_number)

	def e_number(message):
		global name, number
		number = message.text
		msg = bot.send_message(message.chat.id, 'Введите количество персон:')
		bot.register_next_step_handler(msg, e_num_per)

	def e_num_per(message):
		global name, number, num_per
		num_per = message.text
		msg = bot.send_message(message.chat.id, 'Введите время:')
		bot.register_next_step_handler(msg, e_time)

	def e_time(message):
		global name, number, num_per, time, id_user, date
		time = message.text
		id_user = message.chat.id
		date = datetime.date.today()
		msg = bot.send_message(message.chat.id, 'Данные брони:')
		bot.send_message(message.chat.id,
		                 'ФИО: '+str(name)+'\n'+
		                 'Номер: '+str(number)+'\n'+
		                 'Кол. пер.: '+str(num_per)+'\n'+
		                 'Время: '+str(time)+'\n'+
		                 'Дата: '+str(date))
		conn = sqlite3.connect('test2.db')
		c1 = conn.cursor()
		c1.execute(
			"INSERT INTO reservation (id_user,name,number,num_per,time,date) VALUES ('%s','%s','%s','%s','%s','%s')"
			% (id_user,name,number,num_per,time,date))
		conn.commit()
		# закрываем соединение с базой
		c1.close()
		conn.close()
		msg = bot.send_message(str(admin[1]), 'Новая бронь'+'\n'+
		                       'ФИО: ' + str(name) + '\n' +
		                       'Номер: ' + str(number) + '\n' +
		                       'Кол. пер.: ' + str(num_per) + '\n' +
		                       'Время: ' + str(time) + '\n' +
		                       'Дата: ' + str(date))
		#id_user, name, number, num_per, time, date = 0

	if c.data == 'Забронировать стол':
		msg = bot.send_message(c.message.chat.id, 'Введите ФИО:')
		bot.register_next_step_handler(msg, e_name)



# Для admin'a
	if c.data == 'Добавить фото в галерею' and admin_active == True:
		msg = bot.delete_message(c.message.chat.id, last_mes)
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name)
					   for name in ['Добавить фото в галерею интерьера','Добавить фото в галерею кухни']])
		msg = bot.send_message(c.message.chat.id, 'Редактирование галереи:', reply_markup=keyboard)

	if c.data == 'Добавить фото в галерею интерьера' and admin_active == True and is_active_change == 0:
		msg = bot.delete_message(c.message.chat.id, last_mes)
		msg = bot.send_message(c.message.chat.id, 'Загрузите фото для добавления в /interior:')
		bot.register_next_step_handler(msg, photoget_interior)


	if c.data == 'Добавить фото в галерею кухни' and admin_active == True and is_active_change == 0:
		msg = bot.delete_message(c.message.chat.id, last_mes)
		msg = bot.send_message(c.message.chat.id, 'Загрузите фото для добавления в /kitchen:')
		bot.register_next_step_handler(msg, photoget_kitchen)

	if c.data == 'Изменить фото' and admin_active == True:
		msg = bot.delete_message(c.message.chat.id, last_mes)
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name)
		               for name in ['Изменить фото в галереи итерьера','Изменить фото в галереи кухни']])
		msg = bot.send_message(c.message.chat.id, 'Изменение фото галереи:',reply_markup=keyboard)

	if c.data == 'Изменить фото в галереи итерьера' and admin_active == True:
		is_active_change = 1
		msg = bot.delete_message(c.message.chat.id, last_mes)
		msg = bot.send_message(c.message.chat.id, 'Введите номер фотографии для замены в /interior:')
		bot.register_next_step_handler(msg, get_number)

	if c.data == 'Изменить фото в галереи кухни' and admin_active == True:
		is_active_change = 2
		msg = bot.delete_message(c.message.chat.id, last_mes)
		msg = bot.send_message(c.message.chat.id, 'Введите номер фотографии для замены в /kitchen:')
		bot.register_next_step_handler(msg, get_number)

	if c.data == 'Удалить фото' and admin_active == True:
		msg = bot.delete_message(c.message.chat.id, last_mes)
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name)
					   for name in ['Удалить фото из галереи интерьера','Удалить фото из галерею кухни']])
		msg = bot.send_message(c.message.chat.id, 'Удаление фото из галереи:', reply_markup=keyboard)

	if c.data == 'Удалить фото из галереи интерьера' and admin_active == True:
		#msg = bot.delete_message(c.message.chat.id, last_mes)
		num_del = int(len(inter))
		msg = bot.send_message(c.message.chat.id, str(num_del))
		file_inter_w = open('inter.pkl', 'wb')
		inter.pop()
		pickle.dump(inter, file_inter_w)
		file_inter_w.close
		os.remove('galery/interior/' + str(num_del) + '.jpg')
		msg = bot.send_message(c.message.chat.id, 'Фото '+ str(num_del) + '.jpg была удалена из /galery/interior/')


	if c.data == 'Удалить фото из галереи кухни' and admin_active == True:
		#msg = bot.delete_message(c.message.chat.id, last_mes)
		num_del = int(len(kitch))
		msg = bot.send_message(c.message.chat.id, str(num_del))
		file_kitch_w = open('kitch.pkl', 'wb')
		inter.pop()
		pickle.dump(kitch, file_inter_w)
		file_kitch_w.close
		os.remove('galery/kitch/' + str(num_del) + '.jpg')
		msg = bot.send_message(c.message.chat.id, 'Фото '+ str(num_del) + '.jpg была удалена из /galery/kitch/')

'''
	if c.data == 'Прос. брон.' and admin_active == True:
		conn = sqlite3.connect('test2.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM reservation')
		row = cur.fetchone()
		while row is not None:
			msg = bot.send_message(c.message.chat.id,
				"id:" + str(row[0]) + " ID: " + row[1] + " | Имя: " + row[2] + " | Номер: " + row[3] + " | Кол. пер: " +
				row[4] + " | Время: " + row[5] + " | Дата: " + row[6])
			row = c.fetchone()
		cur.close()
		conn.close()
'''


def name(m):
	global admin_active
	if m.text == 'Меню' and admin_active == False:
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name)
					   for name in ['Завтраки','Большой обед','Основное меню','Барная карта','Винная карта','Назад']])
		msg = bot.send_message(m.chat.id, 'Меню ресторана:', reply_markup = keyboard)


	if m.text == 'Бронь' and admin_active == False:
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name)
					   for name in ['Забронировать стол']])
		msg = bot.send_message(m.chat.id, 'Бронирование стола:', reply_markup = keyboard)


	if m.text == 'Галерея' and admin_active == False:
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name)
					   for name in ['Интерьер','Кухня']])
		msg = bot.send_message(m.chat.id, 'Какой галереей Вы интересуетесь?', reply_markup = keyboard)
	if m.text == 'Контанты' and admin_active == False:
		msg = bot.send_message(m.chat.id, 'В «-------»   +-(---)--- -- --')
		msg = bot.send_photo(m.chat.id, photo=open('contacts/1.jpg', 'rb'),caption=''
		+'\n'+'<b>Контакты:</b>'
		+'\n'+'<b>📞 Tелефон:</b>'
		+'\n'+' +0(000)000 00 00 '
		+'\n'
		+'\n'+'<b> 🗺 Адрес:</b> '
		+'\n'+'-----, ----------'
		+'\n'+'----------------- '
		+'\n'
		+'\n'+'<b>🕑 График работы:</b>'
		+'\n'+' --:-- - --:--', parse_mode='html')
		keyboard = types.InlineKeyboardMarkup()
		vk_button = types.InlineKeyboardButton(text = 'Группа в ВК', url = 'https://vk.com')
		keyboard.add(vk_button)
		ok_button = types.InlineKeyboardButton(text = 'Группа в ОК', url = 'https://ok.ru')
		keyboard.add(ok_button)
		bot.send_message(m.chat.id, 'Ссылки на соц. сети:',reply_markup=keyboard)



# Для admin'a
	if m.text == 'Редак. Гал.' and admin_active == True:
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name)
					   for name in['Добавить фото в галерею','Изменить фото','Удалить фото']])
		msg = bot.send_message(m.chat.id, 'Редактирование галереи:', reply_markup=keyboard)
	if m.text == 'Прос. брон.' and admin_active == True:
		msg = bot.send_message(m.chat.id, 'Список забронированных столиков:')
		conn = sqlite3.connect('test2.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM reservation')
		row = cur.fetchone()
		date_now = datetime.date.today()
		while row is not None:
			if str(row[6]) == str(date_now):
				msg = bot.send_message(m.chat.id,
					"id:" + str(row[0]) + '\n' +
					"ID: " + row[1] + '\n' +
					"Имя: " + row[2] + '\n' +
					"Номер: " + row[3] + '\n' +
					"Кол. пер: " + row[4] + '\n' +
					"Время: " + row[5] + '\n' +
					"Дата: " + row[6])
			row = cur.fetchone()
		cur.close()
		conn.close()
	if m.text == 'Выйти' and admin_active == True:
		msg = bot.send_message(m.chat.id, 'Вы вышли из adminpage!!!')
		admin_active = False
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in
					   ['Меню', 'Бронь', 'Галерея', 'Контанты']])
		msg = bot.send_message(m.chat.id,
							   '<b>Добро пожаловать в Ресторан</b>' + '\n' + '\n' + 'Тут вы сможете:' + '\n' +
							   'Просмотреть меню' + '\n' +
							   'Забронировать столик' + '\n' +
							   'Просмотреть Галерею' + '\n' +
							   'Просмотреть контактную информацию', parse_mode='html',
							   reply_markup=keyboard)

@bot.message_handler(content_types=['photo'])  ## Хендлер для фото
def photoget_interior(message):                ## функция обработки приема фото
	global inter
	if os.path.getsize('inter.pkl') > 0:
		file_inter = open('inter.pkl', 'rb')
		inter = pickle.load(file_inter)
		file_inter.close()
	file_inter_w = open('inter.pkl', 'wb')
	if len(inter) == 0:
		n = 1
		inter.append(n)
	else:
		n = len(inter) + 1
		inter.append(str(n))
	pickle.dump(inter, file_inter_w)
	file_inter_w.close

	fileid=(message.photo[2].file_id)      ## Берем объект фото из сообщения иногда меняется с 2 на 3 и наоборот
	bb=bot.get_file(fileid)                ## выкачиваем фаил в переменную
	bb=bb.file_path                        ## находим расположение файла на серверах телеги
	logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+API_TOKEN+"/"+bb).read()   ## загружаем фото из серверов телеги
	f = open('galery/interior/'+str(n)+'.jpg', 'wb')     ## создаем пустой фаил и подготавливаем его к записи galtype - папка где будет храниться фаил.  url - название файла
	f.write(logo)   ## записываем фаил из ссылки
	f.close()     ## закрываем работу с файлом
	msg = bot.send_photo(message.chat.id, photo=open('galery/interior/'+str(n)+'.jpg', 'rb'),caption='Новое фото добавленно в /interior:'+str(n)) ## отсылаем фотку с сервера

def photoget_kitchen(message):                ## функция обработки приема фото
	global kitch
	if os.path.getsize('kitch.pkl') > 0:
		file_kitch = open('kitch.pkl', 'rb')
		kitch = pickle.load(file_kitch)
		file_kitch.close()
	file_kitch_w = open('kitch.pkl', 'wb')
	if len(kitch) == 0:
		n = 1
		kitch.append(n)
	else:
		n = len(kitch) + 1
		kitch.append(str(n))
	pickle.dump(kitch, file_kitch_w)
	file_kitch_w.close

	fileid=(message.photo[2].file_id)      ## Берем объект фото из сообщения иногда меняется с 2 на 3 и наоборот
	bb=bot.get_file(fileid)                ## выкачиваем фаил в переменную
	bb=bb.file_path                        ## находим расположение файла на серверах телеги
	logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+API_TOKEN+"/"+bb).read()   ## загружаем фото из серверов телеги
	f = open('galery/kitchen/'+str(n)+'.jpg', 'wb')     ## создаем пустой фаил и подготавливаем его к записи galtype - папка где будет храниться фаил.  url - название файла
	f.write(logo)   ## записываем фаил из ссылки
	f.close()     ## закрываем работу с файлом
	msg = bot.send_photo(message.chat.id, photo=open('galery/kitchen/'+str(n)+'.jpg', 'rb'),caption='Новое фото добавленно в /kitchen:'+str(n)) ## отсылаем фотку с сервера

def get_number(message):
	global num_change
	global inter
	global kitch
	num_change = int(message.text)
	#bot.send_message(message.chat.id, type(num_change))
	if is_active_change == 1 and num_change <= len(inter):
		msg = bot.send_message(message.chat.id, 'Загрузите фото для замены в /galery/interior/')
		bot.register_next_step_handler(msg, photochange_interior)
	elif is_active_change == 1 and (num_change < 1 and num_change > len(inter)):
		msg = bot.send_message(message.chat.id, 'Нету такого фото в /galery/interior/')

	if is_active_change == 2 and num_change <= len(kitch):
		msg = bot.send_message(message.chat.id, 'Загрузите фото для замены в /galery/kitchen/')
		bot.register_next_step_handler(msg, photochange_kitch)
	elif is_active_change == 2 and (num_change < 1 and num_change > len(kitch)):
		msg = bot.send_message(message.chat.id, 'Нету такого фото в /galery/kitchen/')


def photochange_interior(message):
	global num_change
	fileid=(message.photo[2].file_id)      ## Берем объект фото из сообщения иногда меняется с 2 на 3 и наоборот
	bb=bot.get_file(fileid)                ## выкачиваем фаил в переменную
	bb=bb.file_path                        ## находим расположение файла на серверах телеги
	logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+API_TOKEN+"/"+bb).read()   ## загружаем фото из серверов телеги
	f = open('galery/interior/'+str(num_change)+'.jpg', 'wb')     ## создаем пустой фаил и подготавливаем его к записи galtype - папка где будет храниться фаил.  url - название файла
	f.write(logo)   ## записываем фаил из ссылки
	f.close()     ## закрываем работу с файлом
	msg = bot.send_photo(message.chat.id, photo=open('galery/interior/'+str(num_change)+'.jpg', 'rb'),caption='Фото изменено в /interior:'+str(num_change)) ## отсылаем фотку с сервера
	num_change = 0

def photochange_kitch(message):
	global num_change
	fileid=(message.photo[2].file_id)      ## Берем объект фото из сообщения иногда меняется с 2 на 3 и наоборот
	bb=bot.get_file(fileid)                ## выкачиваем фаил в переменную
	bb=bb.file_path                        ## находим расположение файла на серверах телеги
	logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+API_TOKEN+"/"+bb).read()   ## загружаем фото из серверов телеги
	f = open('galery/kitch/'+str(num_change)+'.jpg', 'wb')     ## создаем пустой фаил и подготавливаем его к записи galtype - папка где будет храниться фаил.  url - название файла
	f.write(logo)   ## записываем фаил из ссылки
	f.close()     ## закрываем работу с файлом
	msg = bot.send_photo(message.chat.id, photo=open('galery/kitch/'+str(num_change)+'.jpg', 'rb'),caption='Фото изменено в /kitch:'+str(num_change)) ## отсылаем фотку с сервера
	num_change = 0
'''
def photodel_interior(message):
	global inter
	if os.path.getsize('inter.pkl') > 0:
		file_inter = open('inter.pkl', 'rb')
		inter = pickle.load(file_inter)
		file_inter.close()
	num_del = len(inter)
	file_path = 'galery/kitchen/' + str(num_del) + '.jpg'
	file_inter_w = open('inter.pkl', 'wb')
	if os.path.isfile(file_path):
		if len(inter) == 0:
			msg = bot.send_message(c.message.chat.id, 'Нет фото в галереи /galery/interior/')
		else:
			del inter[num_del]
			pickle.dump(inter, file_inter_w)
			file_inter_w.close
			os.remove(file_path)
			msg = bot.send_message(c.message.chat.id, 'Файл' + str(num_del) +'.jpg был удален из /galery/interior/')
	else:
		msg = bot.send_message(c.message.chat.id, 'Файл уже удален')
'''
bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
