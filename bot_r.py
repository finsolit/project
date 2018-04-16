import telebot
import time
from telebot import types
import _pickle as pickle
import os
import urllib
import cherrypy
from datetime import datetime
TOKEN ='468533580:AAFn9U5W6FN0mBcm03ZMZz3zuvZoBECUtSY'
bot = telebot.TeleBot(TOKEN)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
			
class photo():
    name=''
    url=''
input = open('photo.pkl', 'rb')
bdphoto = pickle.load(input)
input.close()

class referal():
    id=0
    phone='' 
class userobj():
    id=0
    phone=0
    admin=0
    adminin=0
    photosn=0
    dostavka=0
    dostavkabd=[]
    galtype=''
    galbd=[]
    galbdn=0
    gallook=0
    bron=0
    adminct=0
    admincf=0
    admindf=0
    admindf1=0
    admincm=0
    admin_pass=0
    admintitle=0
    tim=''
    nastavnik=''
    def __init__(self):
        self.dostavkabd = []
        self.galbd=[]
		
		
global bdpol,vizov_ofic,svaz_s_vlad,svazi_tel
svazi_tel=[]
vizov_ofic=[]
svaz_s_vlad=[]
bdpol=[]
input = open('bdpol.pkl', 'rb')
bdpol = pickle.load(input)
input.close()
global adminid, adminpass, adminka, bddostavka, bdbron, passnew
passnew=''
bddostavka=[]
bdbron=[]
input = open('admin.pkl', 'rb')
adminka = pickle.load(input)
input.close()
adminid=adminka[0]
adminpass=adminka[1]
global title
title=''
input = open('title.pkl', 'rb')
title = pickle.load(input)
input.close()
input = open('svazi_tel.pkl', 'rb')
svazi_tel = pickle.load(input)
input.close()
def nomer(b):
    global bdpol
    z=0
    k=-1
    for i in bdpol:
        k+=1
        if bdpol[k].id==b:
            z=k
            return(z)
@bot.message_handler(commands=['start'])

def start(m):
    global bdpol
    hesh=m.chat.id
    z=0
    k=-1
    for i in bdpol:
        k+=1
        if bdpol[k].id==hesh:
            print('lol ti tut uje bil')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['🍽 Меню', '📷 Галерея','📖 Бронь','🚗 Доставка','📞 Контакты','Вызов официанта','Связь с владелцем','Реферальная программа']])
            msg = bot.send_message(m.chat.id, title,reply_markup=keyboard)
            z=1
            return
    if z==0:
        bdpol.append(userobj())
        print(bdpol[-1].id)
        bdpol[-1].id=hesh
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        keyboard.add(button_phone)
        msg = bot.send_message(m.chat.id, 'Добро пожаловать в бот-администратор ресторана «Barashki»! 🎉 🙃 \n \n Для авторизации нажмите кнопку «Отправить мой номер»',
        reply_markup=keyboard)

    global dictvk
@bot.message_handler(commands=['admin'])	
def admin(m):
    global bdpol
    msg = bot.send_message(m.chat.id, 'Добро пожаловать в бот-администратор ресторана «Barashki»! 🎉 🙃\n\nВведите, пожалуйста, пароль администратора.')
    k=nomer(m.chat.id)
    bdpol[k].adminin=1
    
	
@bot.message_handler(content_types=["text"])

def repeat_all_messages(message): 
    name(message)
	
@bot.callback_query_handler(func=lambda c:True)

def inline(c):
    global bdpol,mosn,bdphoto,vizov_ofic,svaz_s_vlad,,svazi_tel
    k=nomer(c.message.chat.id)
    bib=c.message.message_id
	
	
	
	
	
	
	
	#Osnovnoe menu
    if c.data == '👍 Основное меню':
        bdpol[k].galtype='mosn'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[0]
		
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '👶 Детское меню':
        bdpol[k].galtype='mdet'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[1]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🍳 Завтраки':
        bdpol[k].galtype='mzaf'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[2]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🌮 Ланчи':
        bdpol[k].galtype='mlan'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[3]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🍷 Напитки и вина':
        bdpol[k].galtype='mnap'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[4]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '💨 Кальяны':
        bdpol[k].galtype='mkal'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[5]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '☕️ Чайная карта':
        bdpol[k].galtype='mcai'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[6]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '☀ Терраса':
        bdpol[k].galtype='gter'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[7]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🕯 Интерьер':
        bdpol[k].galtype='gint'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[8]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🍗 Кухня':
        bdpol[k].galtype='gkuh'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[9]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)

		
		
		
		
		

    if c.data =='⬅️' and bdpol[k].gallook==1:
        k=nomer(c.message.chat.id)
        msg = bot.delete_message(c.message.chat.id, bib)
        bdpol[k].osn-=1
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        try:
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)	
        except Exception:
            print(len(bdpol[k].galbd))
            bdpol[k].osn=len(bdpol[k].galbd)-1
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data =='➡️' and bdpol[k].gallook==1:
        k=nomer(c.message.chat.id)
        msg = bot.delete_message(c.message.chat.id, bib)
        bdpol[k].osn+=1
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['⬅️','➡️']])
        try:
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)	
        except Exception:
            bdpol[k].osn=0
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    #####konec raboti s polzovatelem
    #####Nachalo raboti s adminom
    if c.data == '🍽 Меню':
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['👍 Основное меню', '👶 Детское меню','🍳 Завтраки','🌮 Ланчи','🍷 Напитки и вина','💨 Кальяны','☕️ Чайная карта']])
       msg = bot.send_message(c.message.chat.id, 'Какое меню отредактировать?',reply_markup=keyboard)
    if c.data == '📷 Галерея':
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['☀ Терраса', '🕯 Интерьер','🍗 Кухня']])
       msg = bot.send_message(c.message.chat.id, 'Какую галерею отредактировать?',reply_markup=keyboard)
    if c.data == '👍 Основное менюad':
        bdpol[k].galtype='mosn'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[0]
        bdpol[k].galbdn=0
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '👶 Детское менюad':
        bdpol[k].galtype='mdet'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[1]
        bdpol[k].galbdn=1
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🍳 Завтракиad':
        bdpol[k].galtype='mzaf'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[2]
        bdpol[k].galbdn=2
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🌮 Ланчиad':
        bdpol[k].galtype='mlan'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[3]
        bdpol[k].galbdn=3
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🍷 Напитки и винаad':
        bdpol[k].galtype='mnap'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[4]
        bdpol[k].galbdn=4
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '💨 Кальяныad':
        bdpol[k].galtype='mkal'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[5]
        bdpol[k].galbdn=5
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '☕️ Чайная картаad':
        bdpol[k].galtype='mcai'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[6]
        bdpol[k].galbdn=6
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '☀ Террасаad':
        bdpol[k].galtype='gter'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[7]
        bdpol[k].galbdn=7
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🕯 Интерьерad':
        bdpol[k].galtype='gint'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[8]
        bdpol[k].galbdn=8
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '🍗 Кухняad':
        bdpol[k].galtype='gkuh'
        bdpol[k].osn=0
        bdpol[k].gallook=1
        bdpol[k].galbd=bdphoto[9]
        bdpol[k].galbdn=9
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data =='⬅️ad' and bdpol[k].gallook==1:
        k=nomer(c.message.chat.id)
        msg = bot.delete_message(c.message.chat.id, bib)
        bdpol[k].osn-=1
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        try:
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)	
        except Exception:
            print(len(bdpol[k].galbd))
            bdpol[k].osn=len(bdpol[k].galbd)-1
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data =='➡️ad' and bdpol[k].gallook==1:
        k=nomer(c.message.chat.id)
        msg = bot.delete_message(c.message.chat.id, bib)
        bdpol[k].osn+=1
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        try:
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)	
        except Exception:
            bdpol[k].osn=0
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '✏ Изменить текстad':
        msg = bot.send_message(c.message.chat.id,'На данный момент текст: '+bdpol[k].galbd[bdpol[k].osn].name+'\nВведите новый текст')
        bdpol[k].adminct=1
    if c.data == '✏ Изменить фотоad':
        msg = bot.send_message(c.message.chat.id,'Пришлите новое фото в формате .jpeg')
        bdpol[k].admincf=1
    if c.data == '➕ Добавитьad':
        msg = bot.send_message(c.message.chat.id,'Введите описание фото')
        bdpol[k].admindf1=1
    if c.data == 'Нетad1':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)        
    if c.data == '✖ Удалитьad':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad1') for name in ['Нет','✖ Удалить']])
        msg = bot.send_message(c.message.chat.id,'Точно удалить фото?',reply_markup=keyboard)
    if c.data == '✖ Удалитьad1':
        if len(bdpol[k].galbd)==1:
            msg = bot.send_message(c.message.chat.id, 'Последнее фото в альбоме нельзя удалять!')
            return
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url)
        os.remove(path)
        del bdpol[k].galbd[bdpol[k].osn]
        bdphoto[bdpol[k].galbdn]=bdpol[k].galbd
        output = open('photo.pkl', 'wb')
        pickle.dump(bdphoto, output, 2)
        output.close()
        bdpol[k].osn-=1
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        try:
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)	
        except Exception:
            print(len(bdpol[k].galbd))
            bdpol[k].osn=len(bdpol[k].galbd)-1
            msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if c.data == '↔ Указать местоad':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['Отмена']])
        msg = bot.send_message(c.message.chat.id,'На данный момент картинка находиться на '+str(bdpol[k].osn+1)+' месте\nНа каком месте ее расположить?(Картинка на место которой вы хотите вставить эту будет сдвинута вправо)',reply_markup=keyboard)
        bdpol[k].admincm=1
    if c.data == 'Отменаad':
        bdpol[k].admincm=0
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(c.message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)	
    if c.data =='📲 Контакты':
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['✏ Изменить']])
       msg = bot.send_message(c.message.chat.id, 'Текущий текст:\n'+title,reply_markup=keyboard)
    if c.data =='✏ Изменить':	 
       msg = bot.send_message(c.message.chat.id, 'Введите новый текст раздела «Контакты».')
       bdpol[k].admintitle=1   
    if c.data =='🔑 Пароли для входа':        
       msg = bot.send_message(c.message.chat.id, 'Введите новый пароль')
       bdpol[k].admin_pass=1        		



################## Arhivi 	   
    if c.data =='3do':
        input = open('dostavka.pkl', 'rb')
        bddostavka = pickle.load(input)
        input.close()
        s=''
        for i in range(1, 4):
            try:
                s+=(bddostavka[-i]+'\n\n')
            except Exception:
                continue
        msg = bot.send_message(c.message.chat.id, s)
        bddostavka=[]
    if c.data =='5do':
        input = open('dostavka.pkl', 'rb')
        bddostavka = pickle.load(input)
        input.close()
        s=''
        for i in range(1, 6):
            try:
                s+=(bddostavka[-i]+'\n\n')
            except Exception:
                continue
        msg = bot.send_message(c.message.chat.id, s)
        bddostavka=[]    
    if c.data =='10do':
        input = open('dostavka.pkl', 'rb')
        bddostavka = pickle.load(input)
        input.close()
        s=''
        for i in range(1, 11):
            try:
                s+=(bddostavka[-i]+'\n\n')
            except Exception:
                continue
        msg = bot.send_message(c.message.chat.id, s)
        bddostavka=[]    		

		
		
    if c.data =='3br':
        input = open('bron.pkl', 'rb')
        bdbron = pickle.load(input)
        input.close()
        s=''
        for i in range(1, 4):
            try:
                s+=(bdbron[-i]+'\n\n')
            except Exception:
                continue
        msg = bot.send_message(c.message.chat.id, s)
        bdbron=[]
    if c.data =='5br':
        input = open('bron.pkl', 'rb')
        bdbron = pickle.load(input)
        input.close()
        s=''
        for i in range(1, 6):
            try:
                s+=(bdbron[-i]+'\n\n')
            except Exception:
                continue
        msg = bot.send_message(c.message.chat.id, s)
        bdbron=[]    
    if c.data =='10br':
        input = open('bron.pkl', 'rb')
        bdbron = pickle.load(input)
        input.close()
        s=''
        for i in range(1, 11):
            try:
                s+=(bdbron[-i]+'\n\n')
            except Exception:
                continue
        msg = bot.send_message(c.message.chat.id, s)
        bdbron=[]  




		
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close()		
		
		
		
def name(m):
    global bdpol
    global title, adminid, adminpass, adminka,vizov_ofic,svaz_s_vlad,,svazi_tel
    global passnew
    k=nomer(m.chat.id)
    bdpol[k].gallook=0
    if bdpol[k].adminct==1:
        bdpol[k].galbd[bdpol[k].osn].name=m.text
        bdphoto[bdpol[k].galbdn]=bdpol[k].galbd
        output = open('photo.pkl', 'wb')
        pickle.dump(bdphoto, output, 2)
        output.close()		
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(m.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
        bdpol[k].adminct=0
        bdpol[k].gallook=1
    if bdpol[k].admintitle==1:
        title=m.text
        output = open('title.pkl', 'wb')
        pickle.dump(title, output, 2)
        output.close()
        msg = bot.send_message(m.chat.id,'Текст изменен на:\n'+title)
        bdpol[k].admintitle=0		
    if 	bdpol[k].admindf1==1:
        bdpol[k].tim=m.text
        bdpol[k].admindf1=0
        bdpol[k].admindf=1
        bdpol[k].gallook=1        
        msg = bot.send_message(m.chat.id,'Пришлите фото в формате .jpeg')
    if bdpol[k].admincm==1:
        bdpol[k].gallook=1	
        try:
            fd=int(m.text)
        except Exception:
            msg = bot.send_message(m.chat.id,'Это число не подходит,попробуйте снова')
            return
        if fd<len(bdpol[k].galbd):
            zs=bdpol[k].galbd[bdpol[k].osn]
            del bdpol[k].galbd[bdpol[k].osn]
            bdpol[k].galbd.insert(fd,zs)
            bdphoto[bdpol[k].galbdn]=bdpol[k].galbd
            output = open('photo.pkl', 'wb')
            pickle.dump(bdphoto, output, 2)
            output.close()
        else:
            msg = bot.send_message(m.chat.id,'Это число не подходит,попробуйте снова')  
            return
        bdpol[k].admincm=0
        msg = bot.send_message(m.chat.id,'Место было изменено')
		
    if bdpol[k].admin_pass==2 and m.text==passnew:
        adminpass=m.text
        adminka[1]=adminpass
        output = open('admin.pkl', 'wb')
        pickle.dump(adminka, output, 2)
        output.close()		
        msg = bot.send_message(m.chat.id,'Пароль изменен 👌')	
        bdpol[k].admin_pass=0
        return		
    if bdpol[k].admin_pass==2:        		
        msg = bot.send_message(m.chat.id,'Пароли не совпадают введите повтор еще раз')	
        bdpol[k].admin_pass=2		
		
		
    if bdpol[k].admin_pass==1:
        passnew=m.text        		
        msg = bot.send_message(m.chat.id,'Повторите пароль')	
        bdpol[k].admin_pass=2

		
		
    if m.text=='🚗 Архив доставок' and m.chat.id==adminid :
       bdpol[k].bron=0
       bdpol[k].dostavka=0       
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'do') for name in ['3','5','10']])
       msg = bot.send_message(m.chat.id, 'Добро пожаловать в архив доставки, какое последнее кол-во доставок отобразить?',reply_markup=keyboard)	
		
		
    if m.text=='📖 Архив бронирования' and m.chat.id==adminid :
       bdpol[k].bron=0
       bdpol[k].dostavka=0       
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'br') for name in ['3','5','10']])
       msg = bot.send_message(m.chat.id, 'Добро пожаловать в архив бронирования, какое последнее кол-во бронирований отобразить?',reply_markup=keyboard)		

    if m.text=='📞 Контакты':
       msg = bot.send_message(m.chat.id, title)
       bdpol[k].bron=0
       bdpol[k].dostavka=0
    if m.text=='🍽 Меню':
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['👍 Основное меню', '👶 Детское меню','🍳 Завтраки','🌮 Ланчи','🍷 Напитки и вина','💨 Кальяны','☕️ Чайная карта']])
       msg = bot.send_message(m.chat.id, 'Каким меню вы интересуетесь?',reply_markup=keyboard)
       bdpol[k].bron=0
       bdpol[k].dostavka=0
    if m.text=='⚙️ Настройки' and m.chat.id==adminid:
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['🔑 Пароли для входа']])
       msg = bot.send_message(m.chat.id, 'Настройки администрирования',reply_markup=keyboard)	
    if m.text=='✏ Редактировать' and m.chat.id==adminid:
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['🍽 Меню', '📷 Галерея','📲 Контакты']])
       msg = bot.send_message(m.chat.id, 'Что вы хотите редактировать?',reply_markup=keyboard)
    if m.text==adminpass and bdpol[k].adminin==1:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['✏ Редактировать', '📖 Архив бронирования','🚗 Архив доставок','⚙️ Настройки']])
        msg = bot.send_message(m.chat.id, 'Пароль введен верно',reply_markup=keyboard)
        adminid=m.chat.id
        adminka=[adminid,adminpass]
        output = open('admin.pkl', 'wb')
        pickle.dump(adminka, output, 2)
        output.close()
        bdpol[k].bron=0
        bdpol[k].dostavka=0
        bdpol[k].adminin=0		
        return
    if bdpol[k].adminin==1:
        msg = bot.send_message(m.chat.id, 'Пароль введен не верно')
        bdpol[k].bron=0
        bdpol[k].dostavka=0
        bdpol[k].adminin=0		
    if m.text=='📷 Галерея':
       keyboard = types.InlineKeyboardMarkup(row_width=1)
       keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['☀ Терраса', '🕯 Интерьер','🍗 Кухня']])
       msg = bot.send_message(m.chat.id, 'Какой галереей вы интересуетесь?',reply_markup=keyboard)
       bdpol[k].bron=0
       bdpol[k].dostavka=0	
# Dostavka 		
    if m.text=='🚗 Доставка':
        bdpol[k].dostavka=1
        bdpol[k].datadost=''
        msg = bot.send_message(m.chat.id, 'Представьтесь, пожалуйста')
        return
    if bdpol[k].dostavka==1:
        bdpol[k].dostavka=2
        bdpol[k].namedost=m.text
        msg = bot.send_message(m.chat.id, 'Очень приятно, '+bdpol[k].namedost+'.\nУкажите блюда, которые хотите заказать и в каком количестве')
        return
    if bdpol[k].dostavka==3 and m.text=='👍 Да':
        bdpol[k].dostavka=2	
        msg = bot.send_message(m.chat.id, 'Укажите блюда которые хотите заказать и в каком количестве')	
        return		
    if bdpol[k].dostavka==3 and m.text=='👎 Нет':
        bdpol[k].dostavka=4
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['🌐 Меню', '📷 Галерея','📖 Забронировать столик','🚗 Доставка','📞 Контакты']])
        msg = bot.send_message(m.chat.id, 'На какой адрес хотите заказать доставку?',reply_markup=keyboard)
        return
    if bdpol[k].dostavka==2:
        bdpol[k].dostavka=3
        bdpol[k].datadost=bdpol[k].datadost+'\n'+m.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['👎 Нет','👍 Да']])
        msg = bot.send_message(m.chat.id,'Добавить еще блюд в заказ?',reply_markup=keyboard)
        return
    if bdpol[k].dostavka==4:
        bdpol[k].dostavka=0
        bdpol[k].adrdost=m.text
        msg = bot.send_message(m.chat.id, 'Спасибо! Ваш заказ сохранен 😊\n\nВы заказали блюда:'+bdpol[k].datadost+'\nНа адрес:\n'+bdpol[k].adrdost+'\n\nВскоре с вами свяжется наш администратор.')
        msg = bot.send_message(adminid, bdpol[k].namedost+' заказал(а) доставку блюд:'+bdpol[k].datadost+'\nНа фдрес: '+bdpol[k].adrdost+'\nТелефон:'+str(bdpol[k].phone)+'\n'+datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
        input = open('dostavka.pkl', 'rb')
        bddostavka = pickle.load(input)
        input.close()
        s=bdpol[k].namedost+' заказал(а) доставку блюд:'+bdpol[k].datadost+'\nНа aдрес: '+bdpol[k].adrdost+'\nТелефон:'+str(bdpol[k].phone)+'\nОформлена доставка: '+datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        bddostavka.append(s)
        output = open('dostavka.pkl', 'wb')
        pickle.dump(bddostavka, output, 2)
        output.close() 

        bddostavka=[]
        return

################################################
# Bronirovanie stolov
    if m.text=='📖 Бронь':
        bdpol[k].bron=1
        msg = bot.send_message(m.chat.id, 'Представьтесь, пожалуйста')
        return
    if bdpol[k].bron==1:
        bdpol[k].bron=2
        bdpol[k].namebron=m.text
        msg = bot.send_message(m.chat.id, 'Очень приятно, '+bdpol[k].namebron+'.\nНа какую дату вы бы хотели забронировать столик?')
        return	
    if bdpol[k].bron==2:
        bdpol[k].bron=3
        bdpol[k].databron=m.text
        msg = bot.send_message(m.chat.id, 'На какое время?')
        return
    if bdpol[k].bron==3:
        bdpol[k].bron=4
        bdpol[k].timebron=m.text
        msg = bot.send_message(m.chat.id, 'Количество персон?')
        return
    if bdpol[k].bron==4:
        bdpol[k].bron=0
        bdpol[k].kolbron=m.text
        msg = bot.send_message(m.chat.id, 'Спасибо! Ваша бронь сохранена 😊\n\nВы заказали столик \nДата: '+bdpol[k].databron+'\nВремя: '+bdpol[k].timebron+'\nКоличество гостей: '+bdpol[k].kolbron+'\nВскоре с вами свяжется наш администратор.')
        msg = bot.send_message(adminid, bdpol[k].namebron+' заказал(а) столик, дата: '+bdpol[k].databron+' На время: '+bdpol[k].timebron+' Будет персон:'+bdpol[k].kolbron+'\n'+'Телефон:'+str(bdpol[k].phone)+'\n'+datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
        s=bdpol[k].namebron+' заказал(а) столик\nДата: '+bdpol[k].databron+'\nВремя: '+bdpol[k].timebron+'\nБудет персон: '+bdpol[k].kolbron+'\n'+'Телефон: '+str(bdpol[k].phone)+'\nОформлено бронирование: '+datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
        input = open('bron.pkl', 'rb')
        bdbron = pickle.load(input)
        input.close()

        bdbron.append(s)
        output = open('bron.pkl', 'wb')
        pickle.dump(bdbron, output, 2)
        output.close()	 
        bdbron=[]		
        return
    if m.text=='Вызов официанта':
        vizov_ofic.append(m.chat.id)
        msg = bot.send_message(m.chat.id, 'Укажите № столика') 
        return()		
    if m.chat.id in vizov_ofic:
        vizov_ofic.remove(m.chat.id)
        msg = bot.send_message(m.chat.id, 'Запрос отправлен')
        msg = bot.send_message(adminid, 'Люди за столом № '+m.text+' вызвали официанта.')	
    if m.text=='Связь с владелцем' :
        svaz_s_vlad.append(m.chat.id)
        msg = bot.send_message(m.chat.id, 'Оставте свою жалобу или предложение и оно дойдет прямиком к владельцу.') 
        return()		
    if m.chat.id in svaz_s_vlad:
        svaz_s_vlad.remove(m.chat.id)
        msg = bot.send_message(m.chat.id, 'Запрос отправлен')
        msg = bot.send_message(adminid, 'Предложение\Жалоба от поситителя: \n'+m.text)	
#################### Referali
    if m.text=='Реферальная программа':
        zuz=0
        for i in range(0,len(svazi_tel)):
            if bdpol[k].id == svazi_tel[i].id:
                for j in range(0,len(svazi_tel)):
                    if bdpol[k].phone==svazi_tel[i].phone:
                        zuz+=1
                msg=bot.send_message(m.chat.id, 'Количество людей которые пришли в ресторан благодаря вам: '+zuz)
                return()
        msg=bot.send_message(m.chat.id, 'Напишите телефон того, кто пригласил вас в бот или напишите свой если нашли меня сами.(Телефон писать в формате +7)')
        svazi_tel.append(referal())
        svazi_tel[-1].id=bdpol[k].id
        return()
    for H in range(0,len(svazi_tel)):
        if svazi_tel[H].id==bdpol[k].id and svazi_tel[H].phone='':
           svazi_tel[H].phone==m.text
           output = open('svazi_tel.pkl', 'wb')
           pickle.dump(svazi_tel, output, 2)
           output.close()	
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close()
#########################################################################
		
		
		
		
@bot.message_handler(content_types=["contact"])
def check_chatid(message):
    print(message.contact.phone_number)
    global bdpol
    global title
    k=nomer(message.chat.id)
    bdpol[k].phone='+'+str(message.contact.phone_number)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['🍽 Меню', '📷 Галерея','📖 Бронь','🚗 Доставка','📞 Контакты']])
    msg = bot.send_message(message.chat.id, title ,reply_markup=keyboard)
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close()

    
	
	
@bot.message_handler(content_types=['photo'])
def photoget(message):
    k=nomer(message.chat.id)
    if bdpol[k].admincf==1:	
        fileid=(message.photo[3].file_id)
        bb=bot.get_file(fileid)
        bb=bb.file_path
        logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
        f = open(bdpol[k].galtype+"/"+bdpol[k].galbd[bdpol[k].osn].url, "wb")
        f.write(logo)
        f.close()
        bdpol[k].admincf=0
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
    if bdpol[k].admindf==1:	
        fileid=(message.photo[3].file_id)
        bb=bot.get_file(fileid)
        bb=bb.file_path
        logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
        nk=str(int(time.time()))
        f = open(bdpol[k].galtype+"/"+nk+'.jpg', "wb")
        f.write(logo)
        f.close()
        bdpol[k].galbd.append(photo())
        bdpol[k].galbd[-1].name=bdpol[k].tim
        bdpol[k].galbd[-1].url=nk+'.jpg'
        bdphoto[bdpol[k].galbdn]=bdpol[k].galbd
        output = open('photo.pkl', 'wb')
        pickle.dump(bdphoto, output, 2)
        output.close()	
        bdpol[k].admindf=0
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'ad') for name in ['⬅️','➡️','✏ Изменить текст','✏ Изменить фото','➕ Добавить','✖ Удалить','↔ Указать место']])
        msg = bot.send_photo(message.chat.id, photo=open(bdpol[k].galtype+'/'+bdpol[k].galbd[bdpol[k].osn].url, 'rb'),caption=bdpol[k].galbd[bdpol[k].osn].name,reply_markup=keyboard)
        
	
	
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
			
			
bot.remove_webhook()
bot.set_webhook('https://185.86.76.249/KKKK/') # Отут букавки делай похуй какие, только скажи мне какие) AAAA, ZZZZ, CCCC уже заняты)

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 7775,  #7771, 7772, 7773 уже заняты, клепай сюда с 4 и дальше)
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})