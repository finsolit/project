
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import telebot
import re
from telebot import types
import sqlite3
import _pickle as pickle
import cherrypy
TOKEN = '551719910:AAGyahWRGa07uIXWQp8VA04LNJIqFNH_i5s'
WEBHOOK_HOST = '95.46.98.126'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)
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
class userobj():
    adminin=0
    id=0
    is_admin=0
    add_group=0	
    comand_type=0
    chek_id=0
    chek_teg=0
    comand_menu=''
    phone=''
    bun=0
    buntime=0
    is_new=0
global doublesid, doblist
global bunlist
doublesid=[]
doblist=[]
class doubles():
    id=0
    last_message=''
    group_id=0
    last_messageid=0
class tag():
    name=''
    words=[]
    is_complex=0
    def __init__(self):
        self.words=[]
    
class administrator():
    id=0
    tid=0
    change_title=0
    change_opisanie=0
    change_tags=0
    change_options=0
    change_link=0
    change_admin=0
    change_word=0
global conn	

admis=administrator()
comands=[1,1,1]	
comands_name=['Поиск по теме','Рейтинг пользователя','Отзывы о пользователе']
class group():
    id=0
    title=''
    opisanie=''
    tags=[]
    options=[]	
    link=''
    administrator=''
    comands=comands
    def __init__(self):
        self.tags=[]
        self.options=[]	
	 
global groups,new_group,adminid
adminid=0
new_group=group()
groups=[]	
global admin_password
admin_password='QWE123'
global bdpol
bdpol=[]
input = open('bdpol.pkl', 'rb')
bdpol = pickle.load(input)
input.close()	
input = open('groups.pkl', 'rb')
groups = pickle.load(input)
input.close()

def nomer(b):
    global bdpol
    z=0
    k=-1
    for i in bdpol:
        k+=1
        if bdpol[k].id==b:
            z=k
            print(b)
            return(z)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
    global bdpol
    bib=message.message_id
    if message.chat.id<0:
        msg = bot.delete_message(message.chat.id, bib)
        return()
    hesh=message.chat.id
    z=0
    k=-1
    for i in bdpol:
        k+=1
        if bdpol[k].id==hesh:
            print('lol ti tut uje bil')
            bdpol[k].bun=0
            if bdpol[k].is_admin==1:
               bdpol[k].is_admin=0              
            z=1
            if bdpol[k].is_new==0:
                if message.from_user.username==None:
                 keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                 keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Поставить юзернейм']]) 
                 button_phone = types.KeyboardButton(text='Отправить свой контакт', request_contact=True)
                 keyboard.add(button_phone)
                 keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Пусть меня будет сложно найти']]) 
                 msg = bot.send_message(message.chat.id, 'Меня зовут LP_iВot, ежедневно я работаю над созданием и улучшением тематических групп в телеграмм. Немаловажным аспектом функционирования групп, является безопасность и репутация ее участников, поэтому в наших сообществах существует возможность запросить отзывы по каждому участнику за весь период его пребывания в группе. Для того что бы вы могли использовать функционал групп на 100 % Вам необходимо заполнить юзернейм или оставить свои контактные данные, иначе другие участники не смогут писать отзывы об удачной, совместной работе.',parse_mode='HTML',reply_markup=keyboard)            
                 return() 
    if z==0:
        bdpol.append(userobj())
        print(bdpol[-1].id)
        bdpol[-1].id=hesh
        bdpol[-1].is_new=1
        if message.from_user.username==None:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Поставить юзернейм']]) 
            button_phone = types.KeyboardButton(text='Отправить свой контакт', request_contact=True)
            keyboard.add(button_phone)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Пусть меня будет сложно найти']]) 
            msg = bot.send_message(message.chat.id, 'Меня зовут LP_iВot, ежедневно я работаю над созданием и улучшением тематических групп в телеграмм. Немаловажным аспектом функционирования групп, является безопасность и репутация ее участников, поэтому в наших сообществах существует возможность запросить отзывы по каждому участнику за весь период его пребывания в группе. Для того что бы вы могли использовать функционал групп на 100 % Вам необходимо заполнить юзернейм или оставить свои контактные данные, иначе другие участники не смогут писать отзывы об удачной, совместной работе.',parse_mode='HTML',reply_markup=keyboard)            
            return()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])  
    msg = bot.send_message(message.chat.id, 'Добро пожаловать в LP_iВot выберите группу которая соответствует вашим интересам.',parse_mode='HTML',
    reply_markup=keyboard)

	
@bot.message_handler(commands=['admin'])	
def admin(m):
    global bdpol
    if m.chat.id>0:
        msg = bot.send_message(m.chat.id, 'Добро пожаловать в панель администратора!\n\nВведите, пожалуйста, пароль администратора.')
        k=nomer(m.chat.id)
        bdpol[k].adminin=1
    else:
        return()	
	
	
	
@bot.message_handler(commands=['chek_id'])	
def chek_id(m):
    global bdpol
    print(m.chat.id)
    k=nomer(m.from_user.id)
    if bdpol[k].is_admin==1:
        if bdpol[k].add_group==2:
            msg = bot.send_message(m.chat.id, 'Хорошо вы привязали id чата')
            new_group.id=m.chat.id
            bdpol[k].add_group=3
            msg = bot.send_message(m.from_user.id, 'Прекрасно, теперь напишите мне список правил общения в группе.') 
            return()			
    bib=m.message_id
    if m.chat.id<0:
        msg = bot.delete_message(m.chat.id, bib)
        return()			
        
	
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    name(message)	
	
	
	
@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    global bdpol, conn
    k=nomer(c.message.chat.id)
    if 'Изменить название' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=c.data[i+1:]
        msg = bot.send_message(c.message.chat.id, 'Сейчас название паблика в боте: '+groups[int(gid)].title+'\nВведите новое название.')
        admis.id=int(gid)
        admis.change_title=1
    if 'Изменить правила' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=c.data[i+1:]
        msg = bot.send_message(c.message.chat.id, 'Сейчас правила: '+groups[int(gid)].opisanie+'\nВведите новые правила.')
        admis.id=int(gid)
        admis.change_opisanie=1
    if 'Изменить ссылку' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=c.data[i+1:]
        msg = bot.send_message(c.message.chat.id, 'Сейчас cсылка: '+groups[int(gid)].link+'\nВведите новую ссылку.')
        admis.id=int(gid)
        admis.change_link=1
    if 'Изменить темы' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
        tz=''
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(groups[gid].tags)):
            tz=tz+groups[gid].tags[i].name+'\n'
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='tema'+str(i)) for name in [groups[gid].tags[i].name]])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+str(gid)) for name in ['Добавить тему','Добавить сложную тему','Удалить тему']])
        msg = bot.send_message(c.message.chat.id, 'На данный момент темы в группе: \n'+tz+'\nКакую тему изменить?',reply_markup=keyboard)	
        admis.id=int(gid)
########################## prosmotr tem
    if 'Темы' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
        tz=''
        for i in range(0,len(groups[gid].tags)):
            tz=tz+'\nНазвание: '+groups[gid].tags[i].name+'\n'
            for j in range(0,len(groups[gid].tags[i].words)):
                    tz=tz+groups[gid].tags[i].words[j]+'\n'             
        msg = bot.send_message(c.message.chat.id, 'Темы состоят из слов, одно из этих слов обязательно должно быть в сообщении для присвоении ему темы:'+tz)	        
########################## Izmenenie temi
    if 'tema' in c.data:
        tid=int(c.data[4:])
        admis.tid=tid
        gid=admis.id
        tz=''		
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addword'+str(tid)) for name in ['Добавить слова']])
        for i in range(0,len(groups[gid].tags[tid].words)):
            tz=tz+groups[gid].tags[tid].words[i]+'\n'
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='worl'+str(i)) for name in [groups[gid].tags[tid].words[i]]])      
        msg = bot.send_message(c.message.chat.id, 'На данный момент в теме такие слова: \n'+tz+'\nНажмите на слово что-бы удалить его из темы.',reply_markup=keyboard)   
########################## Udalenie slova
    if 'worl' in c.data:
        wid=int(c.data[4:])
        try:
            del groups[admis.id].tags[admis.tid].words[wid]
            msg = bot.send_message(c.message.chat.id, 'Удаление слова прошло успешно') 
        except Exception:
            msg = bot.send_message(c.message.chat.id, 'В удалении слова что-то пошло не так')   
########################## dobavlenie slova
    if 'addword' in c.data:
        msg = bot.send_message(c.message.chat.id, 'Введите новые слова через пробел') 
        admis.change_word=1       	
########################## Izmenit administratora
    if 'Указать администратора' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
        admis.id=int(gid)
        admis.change_admin=1
        msg = bot.send_message(c.message.chat.id, 'Пожалуйста введите никнейм администратора.(без @)')	        
########################## Izmenenie comand
    if 'Изменить команды' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        tz=''
        for i in range(0,len(groups[gid].comands)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='coma'+str(i)) for name in [comands_name[i]]])
            if groups[gid].comands[i]==1:
                tz=tz+comands_name[i]+': Работает\n' 
            else:
                tz=tz+comands_name[i]+': Отключено\n' 			
        msg = bot.send_message(c.message.chat.id, 'Команды:\n'+tz,reply_markup=keyboard)	
        admis.id=int(gid)	

    if 'coma' in c.data:
        print(c.data[4:])
        off=int(c.data[4:])
        gid=admis.id
        if groups[admis.id].comands[off]==1 :
            groups[admis.id].comands[off]=0
        else:
            groups[admis.id].comands[off]=1
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        tz=''
        for i in range(0,len(groups[gid].comands)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='coma'+str(i)) for name in [comands_name[i]]])
            if groups[gid].comands[i]==1:
                tz=tz+comands_name[i]+': Работает\n' 
            else:
                tz=tz+comands_name[i]+': Отключено\n' 			
        msg = bot.send_message(c.message.chat.id, 'Команды:\n'+tz,reply_markup=keyboard)				
####################################################
    if 'Добавить сложную тему' in c.data:
        msg = bot.send_message(c.message.chat.id, ' Добавте тему сообщений и слова к теме.\n1-е слово название темы, остальные слова через пробел которые входят в тему. \n Все слова в этой теме толжны входить в сообщение.')	        	
        admis.change_tags=2			
    if 'Добавить тему' in c.data:
        msg = bot.send_message(c.message.chat.id, ' Добавте тему сообщений и слова к теме.\n1-е слово название темы, остальные слова через пробел которые входят в тему')	        	
        admis.change_tags=1		
    if 'Удалить тему' in c.data:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for i in range(0,len(groups[admis.id].tags)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='tag†'+str(i)) for name in [groups[admis.id].tags[i].name]])
        msg = bot.send_message(c.message.chat.id, 'Какую тему удалить?',reply_markup=keyboard)	        	
    if 'tag†' in c.data:
        ip=int(c.data[4:])
        try:
            del groups[admis.id].tags[ip]
            msg = bot.send_message(c.message.chat.id, 'Удаление прошло успешно.')	
        except Exception:
            msg = bot.send_message(c.message.chat.id, 'Ошибка удаления')	  
    if 'Удалить группу' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
        admis.id=gid
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'*') for name in ['Да','Нет']])
        msg = bot.send_message(c.message.chat.id, 'Точно удалить группу?',reply_markup=keyboard)	
    if 'Да' in c.data and c.data[-1]=='*':	
        del groups[admis.id]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Добавить группу']])
        for i in range(0,len(groups)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])  
        msg = bot.send_message(c.message.chat.id, 'Удаление группы было закончено',reply_markup=keyboard)  
    if 'Нет' in c.data and c.data[-1]=='*':			
        msg = bot.send_message(c.message.chat.id, 'Удаление группы было отменено',reply_markup=keyboard) 
############################ Vstuplenie v grupu
    if 'Перейти в группу' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
        msg = bot.send_message(c.message.chat.id, 'Вот ссылка для перехода в группу: '+str(groups[gid].link)+'\nО правилах общения, а также дополнительных возможностях доступных в группе вы можете узнать у  LP_iВot') 
########################### ispolzovanie comand
    if 'Команды' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        tz=''
        for i in range(0,len(groups[gid].comands)):
            if groups[gid].comands[i]==1:
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='exes'+str(i)+'†'+str(gid)) for name in [comands_name[i]]])			
        msg = bot.send_message(c.message.chat.id, 'Команды:'+tz,reply_markup=keyboard)	           
##################################### Komanda vipolnenie
    if 'exes' in c.data:
        for i in range(0,len(c.data)):
                if c.data[i]=='†':
                    gid=int(c.data[i+1:])
                    cid=int(c.data[4:i])
        bdpol[k].chek_id=gid
        if cid==0:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in range(0,len(groups[gid].tags)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='com1'+str(i)) for name in [groups[gid].tags[i].name]])
            msg = bot.send_message(c.message.chat.id, 'По какой теме осуществлять поиск?',reply_markup=keyboard)	             		
        if cid==1:
            msg = bot.send_message(c.message.chat.id, 'Введите юзернейм:')	
            bdpol[k].comand_type=1
        if cid==2:
            msg = bot.send_message(c.message.chat.id, 'Введите юзернейм:')	
            bdpol[k].comand_type=2			

    if 'com1' in c.data:
        cid=int(c.data[4:])
        bdpol[k].chek_teg=cid
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comi'+str(0)) for name in ['1 день']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comi'+str(1)) for name in ['3 дня']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comi'+str(2)) for name in ['Неделя']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comi'+str(3)) for name in ['Месяц']])
        msg = bot.send_message(c.message.chat.id, 'По какому времени осуществлять поиск?',reply_markup=keyboard)		
    
    if 'comi' in c.data:
        date=int(c.data[4:])
        tz=comand1(groups[bdpol[k].chek_id].id,groups[bdpol[k].chek_id].tags[bdpol[k].chek_teg].name,date)		
        print(tz)
        msg = bot.send_message(c.message.chat.id, tz)
		
    if 'comz' in c.data:
        date=int(c.data[4:])
        tz=comand3(groups[bdpol[k].chek_id].id,bdpol[k].comand_menu,date)		
        print(tz)
        msg = bot.send_message(c.message.chat.id, tz)
    output = open('groups.pkl', 'wb')
    pickle.dump(groups, output, 2)
    output.close()
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close()	
    return()
	
		
 
 
 
def name(m):
    global bdpol,adminid, conn
    global doublesid, doblist
    print(doublesid)
############################## pusto
    if m.chat.id<0:
        print(m.from_user.id, m.text)
        for i in range(0,len(groups)):
            if m.chat.id == groups[i].id:
                ids=i
        if len(groups[ids].tags)==0:
            return()
############################## proverka na dublikat
    if m.chat.id<0:
        print(m.text)
        for i in range(0,len(groups)):
            if m.chat.id == groups[i].id:
                ids=i
        if m.from_user.username==groups[ids].administrator:
            return()
        if m.from_user.id==adminid:
            return()
        if m.from_user.id not in doublesid:
            doublesid.append(m.from_user.id)
            new_dob=doubles()
            new_dob.id= m.from_user.id
            new_dob.last_message=m.text
            new_dob.group_id=m.chat.id
            new_dob.last_messageid=m.message_id
            doblist.append(new_dob)
        else:
            for i in range(0,len(doblist)):
                if m.from_user.id == doblist[i].id and m.chat.id!=doblist[i].group_id and m.text== doblist[i].last_message:
                    print('bingo!')
                    try:
                       msg = bot.delete_message(m.chat.id,m.message_id) 
                       msg = bot.delete_message(doblist[i].group_id,doblist[i].last_messageid) 
                    except Exception:
                       a=''	
                    bunlist(m.from_user.id,m.chat.id)	
                    return()
            
                doblist[i].id= m.from_user.id
                doblist[i].last_message=m.text
                doblist[i].group_id=m.chat.id
                doblist[i].last_messageid=m.message_id          					
############################## Proverka i udalenie soobshenia
    bib=m.message_id
    if m.chat.id<0:
        for i in range(0,len(groups)):
            if m.chat.id == groups[i].id:
                ids=i
        if m.from_user.username==groups[ids].administrator:
            return()
    if m.from_user.id!=adminid:
        if m.chat.id<0:
            for i in range(0,len(groups)):
                if m.chat.id == groups[i].id:
                    ids=i
            if m.entities!=None	:			
                for i in range(0,len(m.entities)):
                    if m.entities[i] in ["url", "text_link"]:
                        msg = bot.delete_message(m.chat.id, bib)  
                        bunlist(m.from_user.id,m.chat.id)
                        return()
            if m.reply_to_message!=None:
                stron='  Отзыв о: '
                if m.reply_to_message.from_user.username == None:
                    for i in range(0,len(bdpol)):
                        if m.from_user.id == bdpol[i].id and bdpol[i].phone!='':
                            stron=stron+bdpol[i].phone
                    stron=stron+m.reply_to_message.from_user.first_name+' '+m.reply_to_message.from_user.last_name
                else:
                    stron=stron+'@'+m.reply_to_message.from_user.username
                m.text=m.text+stron	
            if 'отзыв' in m.text.lower():
                        conn = sqlite3.connect('BD.db')	
                        cursor = conn.cursor()
                        if m.from_user.username == None:
                            for i in range(0,len(bdpol)):
                                if m.from_user.id == bdpol[i].id and bdpol[i].phone!='':
                                    cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":bdpol[i].phone, "tag":'отзыв'})
                                    conn.commit()
                                    conn.close()
                                    return()    
                            cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":m.from_user.first_name+' '+m.from_user.last_name, "tag":'отзыв'})
                            conn.commit()
                            conn.close()
                            return()                        								
                        else:
                            cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":'@'+m.from_user.username, "tag":'отзыв'})
                            conn.commit()
                            conn.close()
                            return()                			
            for i in range(0,len(groups[ids].tags)):
                for j in range(0,len(groups[ids].tags[i].words)):

                    if 	groups[ids].tags[i].words[j] in m.text.lower() and groups[ids].tags[i].is_complex==0:
                        conn = sqlite3.connect('BD.db')	
                        cursor = conn.cursor()
                        if m.from_user.username == None:
                            for i in range(0,len(bdpol)):
                                if m.from_user.id == bdpol[i].id and bdpol[i].phone!='':
                                    cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":bdpol[i].phone, "tag":groups[ids].tags[i].name})
                                    conn.commit()
                                    conn.close()
                                    return()    
                            cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":m.from_user.first_name+' '+m.from_user.last_name, "tag":groups[ids].tags[i].name})
                            conn.commit()
                            conn.close()
                            return()                        								
                        else:
                            cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":'@'+m.from_user.username, "tag":groups[ids].tags[i].name})
                            conn.commit()
                            conn.close()
                            return()
                    elif groups[ids].tags[i].words[j] in m.text.lower() and groups[ids].tags[i].is_complex==1:
                        print('da complex')
                        zid=0
                        print(len(groups[ids].tags[i].words))						
                        for cc in range(0,len(groups[ids].tags[i].words)):
                            if groups[ids].tags[i].words[cc] in m.text:
                                zid+=1
                        print(zid)
                        if len(groups[ids].tags[i].words)==zid:
                            conn = sqlite3.connect('BD.db')	
                            cursor = conn.cursor()
                            if m.from_user.username == None:
                                for i in range(0,len(bdpol)):
                                    if m.from_user.id == bdpol[i].id and bdpol[i].phone!='':
                                        cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":bdpol[i].phone, "tag":groups[ids].tags[i].name})
                                        conn.commit()
                                        conn.close()
                                        return()    
                                cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":m.from_user.first_name+' '+m.from_user.last_name, "tag":groups[ids].tags[i].name})
                                conn.commit()
                                conn.close()
                                return()                        								
                            else:
                                cursor.execute("insert into mess values (:gid, :date, :text, :user, :tag) ", {"gid": m.chat.id,"date": m.date, "text":m.text, "user":'@'+m.from_user.username, "tag":groups[ids].tags[i].name})
                                conn.commit()
                                conn.close()
                                return()
            msg = bot.delete_message(m.chat.id, bib)
            bunlist(m.from_user.id,m.chat.id)
            return()	
    else:
        if m.chat.id<0:
            return()
    k=nomer(m.chat.id)
################################# Pervii vhod
    if m.text ==  'Поставить юзернейм':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Я поставил юзернейм']]) 
            button_phone = types.KeyboardButton(text='Отправить свой контакт', request_contact=True)
            keyboard.add(button_phone)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Пусть меня будет сложно найти']]) 
            msg = bot.send_document(m.chat.id, 'https://i.makeagif.com/media/3-23-2018/sXDTus.gif',caption='Вот как поставить юзернейм' , reply_markup=keyboard)   
            return()
    if m.text ==  'Я поставил юзернейм':
        if m.from_user.username==None:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Я поставил юзернейм']]) 
            button_phone = types.KeyboardButton(text='Отправить свой контакт', request_contact=True)
            keyboard.add(button_phone)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Пусть меня будет сложно найти']]) 
            msg = bot.send_message(m.chat.id, 'Вы не выставили юзернейм.',parse_mode='HTML',reply_markup=keyboard)            
            return()
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])  
        msg = bot.send_message(m.chat.id, 'Добро пожаловать в LP_iВot выберите группу которая соответствует вашим интересам.',parse_mode='HTML',
        reply_markup=keyboard)
        return()
    if m.text == 'Пусть меня будет сложно найти':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])  
        msg = bot.send_message(m.chat.id, 'Добро пожаловать в LP_iВot выберите группу которая соответствует вашим интересам.',parse_mode='HTML',
        reply_markup=keyboard)      
######################################################## comanda 2	
    if bdpol[k].comand_type==1:
        bdpol[k].comand_type=0
        nom=comand2(groups[bdpol[k].chek_id].id,m.text)
        msg = bot.send_message(m.chat.id, 'Количество отзывов о искомом пользователе: '+str(nom)) 
################################# Comanda #3
    if bdpol[k].comand_type==2:
        bdpol[k].comand_type=21
        bdpol[k].comand_menu=m.text
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comz'+str(0)) for name in ['1 месяц']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comz'+str(1)) for name in ['3 месяца']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comz'+str(2)) for name in ['6 месяцев']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comz'+str(3)) for name in ['9 месяцев']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comz'+str(4)) for name in ['Год']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='comz'+str(5)) for name in ['Все время']])
        msg = bot.send_message(m.chat.id, 'По какому времени осуществлять поиск?',reply_markup=keyboard) 
################################# Dobavlenie tem
    if admis.change_tags==1:
        if bdpol[k].is_admin==1:
            admis.change_tags=0
        tags=[]
        n=0
        trr=m.text+' '
        for i in range(0,len(trr)):
            if trr[i]==' ':
                tags.append(trr[n:i])
                n=i+1
        print(tags)
        new_tag=tag()
        new_tag.name=tags[0]
        for i in range (1,len(tags)):
            new_tag.words.append(tags[i])
        groups[admis.id].tags.append(new_tag)
        msg = bot.send_message(m.chat.id, 'Добавление темы прошло успешно')
        return()
    if admis.change_tags==2:
        if bdpol[k].is_admin==1:
            admis.change_tags=0
        tags=[]
        n=0
        trr=m.text+' '
        for i in range(0,len(trr)):
            if trr[i]==' ':
                tags.append(trr[n:i])
                n=i+1
        print(tags)
        new_tag=tag()
        new_tag.name=tags[0]
        new_tag.is_complex=1
        for i in range (1,len(tags)):
            new_tag.words.append(tags[i])
        groups[admis.id].tags.insert(0,new_tag)
        msg = bot.send_message(m.chat.id, 'Добавление темы прошло успешно')
        return()
####################################### dobavlenie novih slov v temu
    if admis.change_word==1:
        admis.change_word=0
        tags=[]
        n=0
        trr=m.text+' '
        for i in range(0,len(trr)):
            if trr[i]==' ':
                tags.append(trr[n:i])
                n=i+1
        print(tags)
        for i in range (0,len(tags)):
            groups[admis.id].tags[admis.tid].words.append(tags[i])
        msg = bot.send_message(m.chat.id, 'Добавление темы прошло успешно')
        return()
		
#######################################
    if admis.change_title==1:
        if bdpol[k].is_admin==1:
            admis.change_title=0
            groups[admis.id].title=m.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Добавить группу']])
            for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])    
            msg = bot.send_message(m.chat.id, 'Название группы в боте изменено',reply_markup=keyboard)   
    if admis.change_opisanie==1:
        if bdpol[k].is_admin==1:
            admis.change_opisanie=0
            groups[admis.id].opisanie=m.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Добавить группу']])
            for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])    
            msg = bot.send_message(m.chat.id, 'Описание изменено',reply_markup=keyboard)
#############################!~~~~~~~~~~~~~~~~~~~~~~~~			
    if admis.change_admin==1:
        if bdpol[k].is_admin==1:
            admis.change_admin=0
            groups[admis.id].administrator=m.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Добавить группу']])
            for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])    
            msg = bot.send_message(m.chat.id, 'Администратор добавлен',reply_markup=keyboard)  
    if admis.change_link==1:
        if bdpol[k].is_admin==1:
            admis.change_link=0
            groups[admis.id].link=m.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Добавить группу']])
            for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])    
            msg = bot.send_message(m.chat.id, 'Ссылка изменена',reply_markup=keyboard)  
    if bdpol[k].adminin==1:
        if m.text==admin_password:
            bdpol[k].is_admin=1
            bdpol[k].adminin=0
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Добавить группу']])
            for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])    
            msg = bot.send_message(m.chat.id, 'Пароль введен верно. \n\nДобро пожаловать в админ панель.',reply_markup=keyboard)
            adminid=m.chat.id
        else: 
            bdpol[k].adminin=0 
            msg = bot.send_message(m.chat.id, 'Пароль введен не верно.')
        return()
    if bdpol[k].is_admin==1:
        if m.text=='Добавить группу':
            bdpol[k].add_group=1
            msg = bot.send_message(m.chat.id, 'Введите название группы.')    
            return()
    if bdpol[k].add_group==1:
        bdpol[k].add_group=2
        new_group.title=m.text
        msg = bot.send_message(m.chat.id, 'Хорошо теперь создайте группу, сделайте из нее супергруппу, добавте меня в администраторы. Затем напишите команду /chek_id что-бы я понял что это за чат')
        return()
    if bdpol[k].add_group==3:
        bdpol[k].add_group=4
        new_group.opisanie=m.text
        try:
            msg = bot.set_chat_description(new_group.id,'Все правила общения и теги и комнды вы можете узнать у @LP_ibot')
        except Exception:
            print('oi')   

        msg = bot.send_message(m.chat.id, 'Вы добавили описание. Теперь добавте тему сообщений и слова к теме.\n1-е слово название темы, остальные слова через пробел которые входят в тему.\n Или напишите None для оставления бота без тем.')
        return()
    if bdpol[k].add_group==4:
        bdpol[k].add_group=5
        if m.text=='None':
            msg = bot.send_message(m.chat.id, 'Создание первой темы прошло успешно, вы можете добавить еще темы после создания группы в меню настроек группы.\n Теперь введите ссылку на группу в телеграмме.')
            return()            
        tags=[]
        n=0
        trr=m.text+' '
        for i in range(0,len(trr)):
            if trr[i]==' ':
                tags.append(trr[n:i])
                n=i+1
        print(tags)
        new_tag=tag()
        new_tag.name=tags[0]
        for i in range (1,len(tags)):
            new_tag.words.append(tags[i])
        new_group.tags.append(new_tag)
        print(new_group.tags[0].name, new_group.tags[0].words)
        msg = bot.send_message(m.chat.id, 'Создание первой темы прошло успешно, вы можете добавить еще темы после создания группы в меню настроек группы.\n Теперь введите ссылку на группу в телеграмме.')
        return()
    if bdpol[k].add_group==5:
        bdpol[k].add_group=0
        new_group.link=m.text	
        groups.append(new_group)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)		
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Добавить группу']])
        for i in range(0,len(groups)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])  
        msg = bot.send_message(m.chat.id, 'Создание группы было закончено. Все команды были добавлены автоматически, можете изменить настройки в меню группы. Так-же можете добавить администратора что-бы бот не удалял его сообщения.',reply_markup=keyboard)
			
        output = open('groups.pkl', 'wb')
        pickle.dump(groups, output, 2)
        output.close()
        return()		
    if bdpol[k].is_admin==1:
        for i in range(0,len(groups)):
            if m.text==groups[i].title:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                tz=''
                for z in range(0,len(groups[i].tags)):
                    print(groups[i].tags[z].name)
                    tz=tz+groups[i].tags[z].name+' '
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'†'+str(i)) for name in ['Изменить название', 'Изменить правила','Изменить темы','Изменить ссылку','Изменить команды','Указать администратора','Удалить группу']])
                msg = bot.send_message(m.chat.id, 'Название группы: '+groups[i].title+'\nПравила группы: '+groups[i].opisanie+'\nСсылка: '+groups[i].link+'\nТемы: '+tz,reply_markup=keyboard)
########################################### panel polzovatela
    if bdpol[k].is_admin==0:
        for i in range(0,len(groups)):
            if m.text==groups[i].title:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                tz=''
                for z in range(0,len(groups[i].tags)):
                    if groups[i].tags[z].is_complex==1:
                        tz=tz+'Сложная тема '
                    tz=tz+groups[i].tags[z].name+'\n'
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name+'†'+str(i)) for name in ['Перейти в группу','Команды','Темы']])
                msg = bot.send_message(m.chat.id, 'Название группы: '+groups[i].title+'\nПравила группы: '+groups[i].opisanie+'\nТемы: '+tz,reply_markup=keyboard)
    output = open('groups.pkl', 'wb')
    pickle.dump(groups, output, 2)
    output.close()
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close()		
 



def comand1(gid,tag,datel):
    conn = sqlite3.connect('BD.db')	
    cursor = conn.cursor()
    tag='%'+tag+'%'
    date=int(time.time())
    results=[]
    answer=''
    stop=[86400,259200,604800,2592000]
    cursor.execute("SELECT text FROM mess WHERE tag LIKE :tag",{"tag":tag})
    results1 = cursor.fetchall()
    cursor.execute("SELECT date FROM mess WHERE tag LIKE :tag",{"tag":tag})
    results2 = cursor.fetchall()
    cursor.execute("SELECT user FROM mess WHERE tag LIKE :tag",{"tag":tag})
    results3 = cursor.fetchall()
    cursor.execute("SELECT gid FROM mess WHERE tag LIKE :tag",{"tag":tag})
    results4 = cursor.fetchall()
    for i in range(0,len(results1)):
        if (int(str(results4[i])[1:-2]))==gid:        
            if (date-int(str(results2[i])[1:-2]))<stop[datel]:
                answer=answer+'\n\n'+str(results1[i])[2:-3]+' \n'+str(results3[i])[2:-3]
    conn.close() 
    if len(results1)==0:
        answer='Не могу ничего найти'
    return(answer)

def comand2(gid,tag):
    conn = sqlite3.connect('BD.db')	
    cursor = conn.cursor()
    tag='%'+tag+'%'
    date=int(time.time())
    results=[]
    answer=0
    cursor.execute("SELECT text FROM mess WHERE text LIKE :tag",{"tag":tag})
    results1 = cursor.fetchall()
    cursor.execute("SELECT date FROM mess WHERE text LIKE :tag",{"tag":tag})
    results2 = cursor.fetchall()
    cursor.execute("SELECT user FROM mess WHERE text LIKE :tag",{"tag":tag})
    results3 = cursor.fetchall()
    cursor.execute("SELECT gid FROM mess WHERE text LIKE :tag",{"tag":tag})
    results4 = cursor.fetchall()
    for i in range(0,len(results1)):
        if (int(str(results4[i])[1:-2]))==gid:        
                answer=answer+1
    conn.close() 
    if len(results1)==0:
        answer='Не могу ничего найти'
    return(answer)

def comand3(gid,tag,datel):
    conn = sqlite3.connect('BD.db')	
    cursor = conn.cursor()
    tag='%'+tag+'%'
    date=int(time.time())
    results=[]
    answer=''
    print(tag)
    print('Ia comanda #3')
    stop=[2592000,7776000,15552000,23328000,31104000,311040000]
    cursor.execute("SELECT text FROM mess WHERE text LIKE :tag",{"tag":tag})
    results1 = cursor.fetchall()
    cursor.execute("SELECT date FROM mess WHERE text LIKE :tag",{"tag":tag})
    results2 = cursor.fetchall()
    cursor.execute("SELECT user FROM mess WHERE text LIKE :tag",{"tag":tag})
    results3 = cursor.fetchall()
    cursor.execute("SELECT gid FROM mess WHERE text LIKE :tag",{"tag":tag})
    results4 = cursor.fetchall()
    for i in range(0,len(results1)):
        if (int(str(results4[i])[1:-2]))==gid:        
            if (date-int(str(results2[i])[1:-2]))<stop[datel]:
                answer=answer+'\n\n'+str(results1[i])[2:-3]+' \n'+str(results3[i])[2:-3]
    conn.close()
    if len(results1)==0:
        answer='Не могу ничего найти'	
    return(answer)

	
	
	
	
def bunlist(id, group_id):
    print('ok bunlist',id,group_id)
    for i in range(0,len(groups)):
                if group_id == groups[i].id:
                    ids=i
    for i in range(0,len(bdpol)):
        if int(bdpol[i].id) == int(id):
            print(bdpol[i].bun)
            if bdpol[i].bun==0:
                bdpol[i].bun=1
                print("bun 1 raz")
                try:
                    msg =bot.send_message(id,'Вы нарушили правила группы '+groups[ids].title+' пожалуйста ознакомтесь с правилами группы и соблюдайте их. Иначе получите бан.')
                except Exception:
                    a=0
                return()					
            if bdpol[i].bun==1:
                bdpol[i].bun=2
                bdpol[i].buntime=int(time.time())+86400
                try:
                    msg =bot.send_message(id,'Вы нарушили правила группы '+groups[ids].title+' во 2-й раз, вы получаете бан на 1 день')
                    msg =bot.restrict_chat_member(group_id,id,bdpol[i].buntime,False,False,False,False) 
                except Exception:
                    a=0
                return()	
            if bdpol[i].bun==2:
                bdpol[i].bun=3
                bdpol[i].buntime=int(time.time())+259200
                try:
                    msg =bot.send_message(id,'Вы нарушили правила группы '+groups[ids].title+' в 3-й раз, вы получаете бан на 3 дня')
                    msg =bot.restrict_chat_member(group_id,id,bdpol[i].buntime,False,False,False,False) 
                except Exception:
                    a=0
                return()	
            if bdpol[i].bun==3:
                bdpol[i].buntime=int(time.time())+604800
                try:
                    msg =bot.send_message(id,'Вы нарушили правила группы '+groups[ids].title+' больше чем 3 раза, вы получаете бан на неделю')
                    msg =bot.restrict_chat_member(group_id,id,bdpol[i].buntime,False,False,False,False) 
                except Exception:
                    a=0
                return()
    
    bdpol.append(userobj())
    print(bdpol[-1].id)
    bdpol[-1].id=id
    bdpol[-1].bun=1
	

@bot.message_handler(content_types=["contact"])
def check_chatid(message):
    print(message.contact.phone_number)
    global bdpol
    global title
    k=nomer(message.chat.id)
    bdpol[k].phone='+'+str(message.contact.phone_number)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])  
    msg = bot.send_message(message.chat.id, 'Добро пожаловать в LP_ibot выберите группу в которой хотите состоять или уже состоите.',parse_mode='HTML',
    reply_markup=keyboard)
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close() 

@bot.message_handler(content_types=["contact"])
def check_chatid(message):
    print(message.contact.phone_number)
    global bdpol
    global title
    k=nomer(message.chat.id)
    bdpol[k].phone='+'+str(message.contact.phone_number)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0,len(groups)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [groups[i].title]])  
    msg = bot.send_message(message.chat.id, 'Добро пожаловать в LP_ibot выберите группу в которой хотите состоять или уже состоите.',parse_mode='HTML',
    reply_markup=keyboard)
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close() 

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
