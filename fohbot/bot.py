import openpyxl
import time
import os
from datetime import datetime
import urllib
import telebot
import _thread
import sqlite3
import schedule
import buttons_create
import json
import struct
import _pickle as pickle
from telebot import types
import cherrypy


wb = openpyxl.load_workbook(filename = 'leng.xlsx')
sheet = wb['test']
val = sheet.cell(row=1, column=1)
print(val.value)
def  lengstr(leng,strn):
    bb=sheet.cell(row=strn, column=leng).value
    return str(bb)
TOKEN = '502527811:AAFmZk2ZhOrtToLsFprcLzucoPAtIwbYZEY'


WEBHOOK_HOST = '95.46.98.126'
WEBHOOK_PORT = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

#ТУТ БОТ
bot = telebot.TeleBot(TOKEN)

class post():
    user_id=0
    channel_id=0
    text=''
    reactions=[]
    document=''
    document_type=''
    buttons=[]
    buttons_url=[]
    post_id=0
    add_type=''
    pin=0
    mut=0
    saved=0
    delete_time=0
    forse_time=0
    def __init__(self):
        self.buttons_url=[]
        self.buttons=[]	
        self.reactions=[]


global add_channel, add_post, add_post_array,posts,change_post
input = open('posts.pkl', 'rb')
posts = pickle.load(input)
input.close()
add_channel=[]
add_post=[]
add_post_array=[]
change_post=[]
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [lengstr(1,3),lengstr(1,4)]])
    keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [lengstr(1,5),lengstr(1,6)]])
    msg = bot.send_message(message.chat.id, lengstr(1,2),reply_markup=keyboard)

	
	
	
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    name(message)	
	
	
	
@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    global add_channel, add_post, add_post_array, posts,change_post
    ll=1
    bib=c.message.message_id
################################## reakcii
    if 'roact' in c.data:
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                num=int(c.data[5:i])
                res=reactions_forse(bib,c.message.chat.id,c.from_user.id,num)
                if res=='Y':
                    msg =bot.answer_callback_query(c.id,'Ваша реакция принята')
                else:
                    msg =bot.answer_callback_query(c.id,'Вы уже отреагировали на этот пост')                    
                return()                
################################## Kanal 
    if c.data[-1]=='$':
        channel_id=c.data[:-1]
        channel_name=chan_name_func(channel_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        msg = bot.delete_message(c.message.chat.id, bib)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'%') for name in ['Создать публикацию']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'@') for name in ['Мои публикации']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'&') for name in ['Автопостинг']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'*') for name in ['Настройки']])
        msg =bot.send_message(c.message.chat.id, channel_name,reply_markup=keyboard)
        return		
################################# vse kanali
    if c.data =='Все каналы':
        channel_id=c.data[:-1]
        msg = bot.delete_message(c.message.chat.id, bib)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Создать публикацию']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Мои публикации']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Автопостинг']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Настройки']])
        msg =bot.send_message(c.message.chat.id, lengstr(ll,11),reply_markup=keyboard)
        return
############################### dobavlenie posta v kanale		
    if c.data[-1]=='%':
        add_post.append(c.message.chat.id)
        add_post_array.append(post())
        msg = bot.delete_message(c.message.chat.id, bib)
        add_post_array[-1].user_id=c.message.chat.id
        add_post_array[-1].channel_id=int(c.data[:-1])
        add_post_array[-1].post_id=int(posts) 
        posts+=1
        output = open('posts.pkl', 'wb')
        pickle.dump(posts, output, 2)
        output.close() 
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=c.data[:-1]+'!') for name in ['Назад к каналу']])
        msg =bot.send_message(c.message.chat.id, lengstr(ll,12),reply_markup=keyboard) 
        return
############################## otmena dobavlenia posta v kanale		
    if c.data[-1]=='!':
        try:
            add_post.remove(c.message.chat.id)
        except Exception:
            a=0
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==c.message.chat.id:
                if add_post_array[i].saved==0:
                    os.remove("documents/"+add_post_array[i].document)
                del add_post_array[i]
        channel_id=c.data[:-1]
        channel_name=chan_name_func(channel_id)
        msg = bot.delete_message(c.message.chat.id, bib)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'%') for name in ['Создать публикацию']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'@') for name in ['Мои публикации']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'&') for name in ['Автопостинг']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'*') for name in ['Настройки']])
        msg =bot.send_message(c.message.chat.id, channel_name,reply_markup=keyboard)  
        return
################################# spisok publikaci
    if c.data[-1]=='@':
        channel_id=int(c.data[:-1])	
        pos=post_in_channel(channel_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(pos)):
            dd=pos[i][4]
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='selpost'+str(pos[i][0])) for name in [str(dd)]])     
        msg =bot.send_message(c.message.chat.id, 'Список постов у канала:',reply_markup=keyboard) 
        return		
################################# Просмотр сохраненного поста
    if 'selpost' in c.data:
        inm=c.data[7:]
        obj=select_from_saved(inm)
        channel_id=obj.channel_id
        post_id=obj.post_id
        msg = bot.delete_message(c.message.chat.id, bib)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Редактировать',callback_data='selred'+str(post_id)),
        types.InlineKeyboardButton(text='Удалить',callback_data=str(post_id)+'l'),
        types.InlineKeyboardButton(text='Опубликовать',callback_data='selopl'+str(post_id)),
        types.InlineKeyboardButton(text='Запланировать',callback_data=str(post_id)+'l'),
        types.InlineKeyboardButton(text='Назад к списку постов',callback_data=str(channel_id)+'@'))
        if 	obj.document_type=='':				
            msg =bot.send_message(c.message.chat.id, obj.text,reply_markup=keyboard)
        if  obj.document_type=='photo':
            msg =bot.send_photo(c.message.chat.id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard)                    
        if  obj.document_type=='audio':
            msg =bot.send_audio(c.message.chat.id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard)
        if  obj.document_type=='video':
            msg =bot.send_video(c.message.chat.id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard)
        if  obj.document_type=='document':
            msg =bot.send_document(c.message.chat.id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard)
   
        return
################################
    if 'selopl' in c.data:
        inm=c.data[6:]
        obj=select_from_saved(inm)
        channel_id=obj.channel_id
        post_id=obj.post_id 
        keyboard = types.InlineKeyboardMarkup()
        for z in range(0,len(obj.buttons_url)):
            print(obj.buttons[z],obj.buttons_url[z])
            url_button = types.InlineKeyboardButton(text=obj.buttons[z], url=obj.buttons_url[z])
            keyboard.add(url_button)
        if len(obj.reactions)>0:
            keyboard.add(*[types.InlineKeyboardButton(text=name+':0',callback_data='roact'+str(obj.reactions.index(name))+':'+name) for name in obj.reactions])
            			
        if 	obj.mut==1:
            mut=True
        else:
            mut=False	
        if 	obj.document_type=='':				
            msg =bot.send_message(obj.channel_id, obj.text,reply_markup=keyboard,disable_notification=mut)
        if  obj.document_type=='photo':
            msg =bot.send_photo(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)                    
        if  obj.document_type=='audio':
            msg =bot.send_audio(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)
        if  obj.document_type=='video':
            msg =bot.send_video(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)
        if  obj.document_type=='document':
            msg =bot.send_document(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)
   
        joy=msg.message_id
        if len(obj.reactions)>0:
            add_reactions(obj.channel_id,joy,obj.reactions)
        if obj.delete_time>0:
            add_delete_func(joy,obj.channel_id,obj.delete_time)                
        if 	obj.pin==1:
            msg=bot.pin_chat_message(obj.channel_id,joy,disable_notification=mut)
        if obj.saved==0:
                    os.remove("documents/"+obj.document)
        return					
################################# redaktirovanie sohranennogo posta
    if 'selred'	in c.data:
        inm=c.data[6:]
        obj=select_from_saved(inm)
        add_post.append(c.message.chat.id)
        add_post_array.append(obj)   
        keyboard=kukoard(obj.post_id,obj.channel_id)
        msg = bot.delete_message(c.message.chat.id, bib)
        msg =bot.send_message(c.message.chat.id, lengstr(ll,13),reply_markup=keyboard) 
        return	
################################# zaplanirovat		
################################# publikacia posta
    if c.data[-1]=='o':
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                if add_post_array[i].forse_time>0: 
                    inputt = pickle.dumps(add_post_array[i])
                    add_forse_func(add_post_array[i].forse_time,inputt)
                    msg =bot.answer_callback_query(c.id,lengstr(ll,35)) 
                    return
                print(add_post_array[i].channel_id)
                keyboard = types.InlineKeyboardMarkup()
                for z in range(0,len(add_post_array[i].buttons_url)):
                    print(add_post_array[i].buttons[z],add_post_array[i].buttons_url[z])
                    url_button = types.InlineKeyboardButton(text=add_post_array[i].buttons[z], url=add_post_array[i].buttons_url[z])
                    keyboard.add(url_button)
                if len(add_post_array[i].reactions)>0:
                    keyboard.add(*[types.InlineKeyboardButton(text=name+':0',callback_data='roact'+str(add_post_array[i].reactions.index(name))+':'+name) for name in add_post_array[i].reactions])   
                if 	add_post_array[i].mut==1:
                    mut=True
                else:
                    mut=False	
                if 	add_post_array[i].document_type=='':				
                    msg =bot.send_message(add_post_array[i].channel_id, add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)
                if  add_post_array[i].document_type=='photo':
                    msg =bot.send_photo(add_post_array[i].channel_id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)                    
                if  add_post_array[i].document_type=='audio':
                    msg =bot.send_audio(add_post_array[i].channel_id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)
                if  add_post_array[i].document_type=='video':
                    msg =bot.send_video(add_post_array[i].channel_id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)
                if  add_post_array[i].document_type=='document':
                    msg =bot.send_document(add_post_array[i].channel_id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)
   
                joy=msg.message_id
                if len(add_post_array[i].reactions)>0:
                    add_reactions(add_post_array[i].channel_id,joy,add_post_array[i].reactions)
                if add_post_array[i].delete_time>0:
                    add_delete_func(joy,add_post_array[i].channel_id,add_post_array[i].delete_time)                
                if 	add_post_array[i].pin==1:
                    msg=bot.pin_chat_message(add_post_array[i].channel_id,joy,disable_notification=mut)	               
                msg =bot.answer_callback_query(c.id,lengstr(ll,14)) 
                return				
################################# dobavlenie knopok k postu
    if c.data[-1]=='k':
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                add_post_array[i].add_type='buttons'
                msg =bot.send_message(c.message.chat.id,lengstr(ll,15),disable_web_page_preview=True)
                change_post.append(c.message.chat.id)
                return		
################################# vrema publikacii
    if c.data[-1]=='v':
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                add_post_array[i].add_type='vrema'
                msg =bot.send_message(c.message.chat.id,lengstr(ll,33),disable_web_page_preview=True)
                change_post.append(c.message.chat.id)
                return					
################################# dobavlenie reakci				
    if c.data[-1]=='r':
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                add_post_array[i].add_type='reactions'
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addsmile'+name) for name in ['👍👎','😊😄😒','❤😐💔🤢','😄😊😔😱😡']])             
                msg =bot.send_message(c.message.chat.id,lengstr(ll,17),reply_markup=keyboard)
                change_post.append(c.message.chat.id)
                return	
################################ dobavlenie reakcii cherez smaili
    if 'addsmile' in c.data:
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==c.message.chat.id:
                if 	add_post_array[i].add_type=='reactions':
                    smiles=c.data[8:]
                    print(len(smiles))
                    add_post_array[i].reactions=[]
                    for z in range(0,len(smiles)):
                        print(smiles[z])
                        add_post_array[i].reactions.append(smiles[z])
                    post_id=add_post_array[i].post_id
                    channel_id=add_post_array[i].channel_id
                    keyboard = kukoard(post_id,channel_id)
						
                    msg =bot.send_message(c.message.chat.id,lengstr(ll,18),reply_markup=keyboard)
                    print(add_post_array[i].reactions)	
                    change_post.remove(c.message.chat.id)	
                    return	
################################## zakrepit
    if c.data[-1]=='z':
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                if add_post_array[i].pin==0:
                    add_post_array[i].pin=1
                    msg =bot.answer_callback_query(c.id,'Пост будет закреплен')
                else:
                    add_post_array[i].pin=0	
                    msg =bot.answer_callback_query(c.id,'Пост не будет закреплен')					
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id					
                keyboard = kukoard(post_id,channel_id)          
                msg =bot.edit_message_reply_markup(c.message.chat.id,bib,reply_markup=keyboard) 
                return	
################################## uvedomlenia
    if c.data[-1]=='u':
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                if add_post_array[i].mut==0:
                    add_post_array[i].mut=1
                    msg =bot.answer_callback_query(c.id,'Пост не пришлет уведомление')
                else:
                    add_post_array[i].mut=0	
                    msg =bot.answer_callback_query(c.id,'Пост пришлет уведомление')					
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id					
                keyboard = kukoard(post_id,channel_id)          
                msg =bot.edit_message_reply_markup(c.message.chat.id,bib,reply_markup=keyboard) 
                return
################################# udalenie posta
    if c.data[-1]=='d':
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                add_post_array[i].add_type='delete'
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                keyboard.add(
                    types.InlineKeyboardButton(text=lengstr(ll,23),callback_data='addelet'+str(1)),
                    types.InlineKeyboardButton(text=lengstr(ll,24),callback_data='addelet'+str(2)),
                    types.InlineKeyboardButton(text=lengstr(ll,25),callback_data='addelet'+str(3)),
                    types.InlineKeyboardButton(text=lengstr(ll,26),callback_data='addelet'+str(4)),
                    types.InlineKeyboardButton(text=lengstr(ll,27),callback_data='addelet'+str(5)),
                    types.InlineKeyboardButton(text=lengstr(ll,28),callback_data='addelet'+str(6)),
                    types.InlineKeyboardButton(text=lengstr(ll,29),callback_data='addelet'+str(7)),
                    types.InlineKeyboardButton(text=lengstr(ll,30),callback_data='addelet'+str(8)),
                    types.InlineKeyboardButton(text=lengstr(ll,31),callback_data='addelet'+str(9)))
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='<') for name in [lengstr(ll,32)]])					
                msg =bot.send_message(c.message.chat.id,lengstr(ll,22),reply_markup=keyboard)
                change_post.append(c.message.chat.id)
                return
################################# zapis na udalenie
    if 'addelet' in c.data:
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==c.message.chat.id: 
                funcs=int(c.data[7:])
                add_post_array[i].delete_time=funcs	
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id
                keyboard = kukoard(post_id,channel_id)
                print(add_post_array[i].delete_time)						
                msg =bot.send_message(c.message.chat.id,lengstr(ll,18),reply_markup=keyboard)	
                return				
################################# publikacia posta
    if c.data[-1]=='p':
        msg = bot.delete_message(c.message.chat.id, bib)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                print(add_post_array[i].channel_id)
                keyboard = types.InlineKeyboardMarkup()
                for z in range(0,len(add_post_array[i].buttons_url)):
                    print(add_post_array[i].buttons[z],add_post_array[i].buttons_url[z])
                    url_button = types.InlineKeyboardButton(text=add_post_array[i].buttons[z], url=add_post_array[i].buttons_url[z])
                    keyboard.add(url_button)
                if len(add_post_array[i].reactions)>0:
                    keyboard.add(*[types.InlineKeyboardButton(text=name+':0',callback_data='') for name in add_post_array[i].reactions])   
                if 	add_post_array[i].mut==1:
                    mut=True
                else:
                    mut=False	
                if 	add_post_array[i].document_type=='':				
                    msg =bot.send_message(c.message.chat.id, add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)
                if  add_post_array[i].document_type=='photo':
                    msg =bot.send_photo(c.message.chat.id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)                    
                if  add_post_array[i].document_type=='audio':
                    msg =bot.send_audio(c.message.chat.id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)
                if  add_post_array[i].document_type=='video':
                    msg =bot.send_video(c.message.chat.id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut)
                if  add_post_array[i].document_type=='document':
                    msg =bot.send_document(c.message.chat.id, open('documents/'+add_post_array[i].document, 'rb'),caption=add_post_array[i].text,reply_markup=keyboard,disable_notification=mut) 
                keyboard=kukoard(add_post_array[i].post_id,add_post_array[i].channel_id)					
                msg =bot.send_message(c.message.chat.id, lengstr(ll,21),reply_markup=keyboard)	
                return
################################ nachat snachala
    if c.data[-1]=='n':
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                msg = bot.delete_message(c.message.chat.id, bib)
                if obj.saved==0:
                    os.remove("documents/"+add_post_array[i].document)
                add_post_array[i].reactions=[]
                add_post_array[i].buttons=[]
                add_post_array[i].buttons_url=[]
                add_post_array[i].mut=0
                add_post_array[i].pin=0
                add_post_array[i].document=''
                add_post_array[i].document_type=''                
                add_post.append(c.message.chat.id)
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=c.data[:-1]+'!') for name in ['Назад к каналу']])
                msg =bot.send_message(c.message.chat.id, lengstr(ll,12),reply_markup=keyboard) 
                return
################################### sohranenie posta
    if c.data[-1]=='s':
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                    if add_post_array[i].saved==1:
                        msg =bot.answer_callback_query(c.id,'Этот пост уже сохранен')					         
                        return	                        
                    add_post_array[i].saved=1
                    save_post(add_post_array[i].post_id,c.message.chat.id,add_post_array[i].channel_id,add_post_array[i])
                    msg =bot.answer_callback_query(c.id,'Пост сохранен')					         
                    return	
################################### sohranenie posta
    if c.data[-1]=='l':
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                    if add_post_array[i].saved==0:
                        msg =bot.answer_callback_query(c.id,'Этот пост не был сохранен')					         
                        return	                        
                    add_post_array[i].saved=0
                    delete_post(add_post_array[i].post_id)
                    msg =bot.answer_callback_query(c.id,'Пост удален')					         
                    return	
        delete_document(int(c.data[:-1]))       
        delete_post(int(c.data[:-1]))
        msg = bot.delete_message(c.message.chat.id, bib)
        msg =bot.send_message(c.message.chat.id, 'Пост удален') 	
        return		
###################################				
    msg =bot.answer_callback_query(c.id,'Эта функция пока не доступна')     				
    return		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
def name(m):
    global add_channel, add_post, add_post_array, posts,change_post
    ll=1
#####################   Dobavlenie kanala
    if m.text==lengstr(ll,3) or m.text==lengstr(ll,4) or m.text==lengstr(ll,5) or m.text==lengstr(ll,6):
        try:
            add_post.remove(m.chat.id)
        except Exception:
            a=0
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==m.chat.id:
                if add_post_array[i].saved==0:
                    if add_post_array[i].document!='':
                        os.remove("documents/"+add_post_array[i].document)
                del add_post_array[i]
                
    if m.text ==lengstr(ll,3):
        add_channel.append(m.chat.id)
        msg = bot.send_message(m.chat.id,lengstr(ll,7))
        return
    if m.chat.id in add_channel:
        new_id=m.forward_from_chat.id
        all_channel=chek_chan()
        if new_id not in all_channel:
            add_channel_func(m.chat.id,new_id,m.forward_from_chat.title)
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            channel_list=chek_user_channels(m.chat.id)
            for i in range (0,len(channel_list[0])):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_list[0][i])+'$') for name in [channel_list[1][i]]])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Все каналы']])
            msg = bot.send_message(m.chat.id,lengstr(ll,8),reply_markup=keyboard)
            add_channel.remove(m.chat.id)			
        else:
            msg = bot.send_message(m.chat.id,lengstr(ll,9))
            add_channel.remove(m.chat.id)
#####################   moi kanali
    if m.text==lengstr(ll,4):
            channel_list=chek_user_channels(m.chat.id)
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in range (0,len(channel_list[0])):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_list[0][i])+'$') for name in [channel_list[1][i]]])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Все каналы']])
            msg = bot.send_message(m.chat.id,lengstr(ll,10),reply_markup=keyboard)
#####################  dobavlenie texta v novi post
    if m.chat.id in add_post:
        add_post.remove(m.chat.id)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==m.chat.id:
                add_post_array[i].text=m.text
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Добавить кнопки',callback_data=str(post_id)+'k'),
        types.InlineKeyboardButton(text='Добавить реакцию',callback_data=str(post_id)+'r'),
        types.InlineKeyboardButton(text='Опубликовать',callback_data=str(post_id)+'o'),
        types.InlineKeyboardButton(text='Время публикации',callback_data=str(post_id)+'v'),
        types.InlineKeyboardButton(text='Сохранить',callback_data=str(post_id)+'s'),
        types.InlineKeyboardButton(text='Автоудаление',callback_data=str(post_id)+'d'),
        types.InlineKeyboardButton(text='Предпросмотр',callback_data=str(post_id)+'p'),
        types.InlineKeyboardButton(text='Начать сначала',callback_data=str(post_id)+'n'),
        types.InlineKeyboardButton(text='⚪️ Закрепить',callback_data=str(post_id)+'z'),
        types.InlineKeyboardButton(text='⚪️ Уведомления',callback_data=str(post_id)+'u'),
        types.InlineKeyboardButton(text='Удалить пост',callback_data=str(post_id)+'l'),
        types.InlineKeyboardButton(text='Вернуться к каналу',callback_data=str(channel_id)+'!'))
        msg =bot.send_message(m.chat.id, lengstr(ll,13),reply_markup=keyboard) 
############################### shapka izmeneni		
    if m.chat.id in change_post:
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==m.chat.id:
############################### dobavlenie knopok
                if 	add_post_array[i].add_type=='buttons':
                    buttons_take=	buttons_create.buttons(m.text)
                    print(buttons_take)					
                    add_post_array[i].buttons=buttons_take[0]
                    add_post_array[i].buttons_url=buttons_take[1]
                    change_post.remove(m.chat.id)
                    keyboard=kukoard(add_post_array[i].post_id,add_post_array[i].channel_id)					
                    msg =bot.send_message(m.chat.id, lengstr(ll,16),reply_markup=keyboard)					
############################### dobavlenie reakci					
                if 	add_post_array[i].add_type=='reactions':
                    smiles=m.text
                    add_post_array[i].reactions=[]
                    for z in range(0,len(smiles)):
                        add_post_array[i].reactions.append(smiles[z])
                    keyboard =kukoard(add_post_array[i].post_id,add_post_array[i].channel_id)
                    msg =bot.send_message(m.chat.id,lengstr(ll,18),reply_markup=keyboard)
                    print(add_post_array[i].reactions)
                    change_post.remove(m.chat.id)	
                if 	add_post_array[i].add_type=='vrema':
                    dd=m.text
                    add_post_array[i].forse_time=0
                    ss=datetime.strptime(dd, '%d.%m.%Y.%H.%M')
                    print(ss)
                    ll=time.mktime(ss.timetuple())
                    add_post_array[i].forse_time=ll  
                    print(add_post_array[i].forse_time)					
                    keyboard =kukoard(add_post_array[i].post_id,add_post_array[i].channel_id)
                    msg =bot.send_message(m.chat.id,lengstr(ll,34),reply_markup=keyboard)
                    change_post.remove(m.chat.id)					
			
			
def add_delete_func(message_id,channel_id,delete_time):
    conn = sqlite3.connect('Thread.sqlite')
    cursor = conn.cursor()
    tim=[0,3600,10800,21600,43200,86400,172800,604800,1209600,2592000]
    delete_time=tim[delete_time]+int(time.time())
    print(message_id)
    print(channel_id)
    print(delete_time)
    cursor.execute("insert into DELETER values (:message_id, :channel_id, :delete_time) ", {"message_id": message_id,"channel_id": channel_id,"delete_time": delete_time,})
    conn.commit()
    conn.close()    


def add_forse_func(forse_time,message_object):
    conn = sqlite3.connect('Thread.sqlite')
    cursor = conn.cursor()
    cursor.execute("insert into FORSEDER values (:forse_time, :message_object) ", {"forse_time": forse_time,"message_object": message_object,})
    conn.commit()
    conn.close() 	
			
def add_channel_func(user_id,channel_id,title):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
	
    cursor.execute("insert into USERS values (:user_id, :channel_id, :title) ", {"user_id": user_id,"channel_id": channel_id,"title": title,})
    conn.commit()
    conn.close()
		
def chek_chan():
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
	
    array=[]
    cursor.execute("SELECT CHANNEL FROM USERS")
    results = cursor.fetchall()
    for i in range(0,len(results)):
        array.append(results[i][0])
    conn.close()
    print(array)
    return(array)
	
def chek_user_channels(user_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
	
    array=[]
    array1=[]
    cursor.execute("SELECT * FROM USERS WHERE USER = :user_id",{"user_id":user_id})
    results = cursor.fetchall()
    for i in range(0,len(results)):
        array.append(results[i][1])
        array1.append(results[i][2])		
    conn.close()
    print(array,array1)
    res=[]
    res.append(array)
    res.append(array1)	
    return(res)	
	
def chan_name_func(channel_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
	
    cursor.execute("SELECT TITLE FROM USERS WHERE CHANNEL = :channel_id",{"channel_id":channel_id})
    results = cursor.fetchall()
    conn.close()
    print(results)
    return(results)


	
def add_reactions(channel_id,message_id,reactions): 
    conn = sqlite3.connect('Thread.sqlite')
    cursor = conn.cursor()
    aa=[]
    for i in range(0,len(reactions)):
        aa.append(0)
    numbers =pickle.dumps(aa)
    users=[]
    users = pickle.dumps(users)
    reactions=pickle.dumps(reactions)
    cursor.execute("insert into REACTIONS values (:channel_id, :message_id, :users,:reactions,:numbers) ", {"channel_id": channel_id,"message_id": message_id,"users": users,"reactions": reactions,"numbers": numbers})
    conn.commit()
    conn.close()   
  
def  reactions_forse(message_id,cennel_id,user_id,num):  
    conn = sqlite3.connect('Thread.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM REACTIONS WHERE CHENNEL_ID = :cennel_id AND MESSAGE_ID = :message_id",{"cennel_id":cennel_id,"message_id":message_id})
  
    results = cursor.fetchall()	    
    conn.close()
    users=pickle.loads(results[0][2])
    reactions=pickle.loads(results[0][3])
    numbers=pickle.loads(results[0][4])
    if user_id not in users:
        numbers[num]+=1
        users.append(user_id)
        keyboard = types.InlineKeyboardMarkup()        
        keyboard.add(*[types.InlineKeyboardButton(text=str(reactions[i])+':'+str(numbers[i]),callback_data='react'+str(i)+':'+str(reactions[i])) for i in range(0,len(reactions))]) 
        msg =bot.edit_message_reply_markup(cennel_id,message_id,reply_markup=keyboard)		
		

        conn = sqlite3.connect('Thread.sqlite')
        cursor = conn.cursor()
        numbers =pickle.dumps(numbers)
        users = pickle.dumps(users)
        reactions=pickle.dumps(reactions)
        cursor.execute("UPDATE REACTIONS SET USRES = :users, NUMBERS = :numbers WHERE CHENNEL_ID = :cennel_id AND MESSAGE_ID = :message_id ", {"cennel_id": cennel_id,"message_id": message_id,"users": users,"numbers": numbers})
        conn.commit()
        conn.close()  
        return('Y')
    else:
        return('N')	
  
  
def save_post(post_id,user_id,channel_id,postr):
    conn = sqlite3.connect('SAVES.sqlite')
    cursor = conn.cursor()
    inputt = pickle.dumps(postr)
    times=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(times)
    cursor.execute("insert into SAVED_POST values (:post_id, :user_id, :channel_id, :message_object, :time) ", {"post_id": post_id,"user_id": user_id,"channel_id": channel_id,"message_object": inputt,"time": times,})
    conn.commit()
    conn.close()   
  
  
def delete_post(post_id):
    conn = sqlite3.connect('SAVES.sqlite')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SAVED_POST WHERE POST_ID = :post_id",{"post_id":post_id})
    conn.commit()    
    conn.close()   
  
def delete_document(post_id):  
    conn = sqlite3.connect('SAVES.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM SAVED_POST WHERE POST_ID = :cennel_id ",{"cennel_id":post_id})
  
    results = cursor.fetchall()	
    obj=pickle.loads(results[0][3]  )
    try:
       os.remove("documents/"+obj.document) 
    except Exception:
       zz=1
    conn.close() 
	
def post_in_channel(channel_id):
    conn = sqlite3.connect('SAVES.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM SAVED_POST WHERE CHANNEL_ID = :cennel_id ",{"cennel_id":channel_id})
  
    results = cursor.fetchall()	    
    conn.close() 
    return(results)	
  
  
  
def select_from_saved(inm):
    conn = sqlite3.connect('SAVES.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM SAVED_POST WHERE POST_ID = :cennel_id ",{"cennel_id":inm})
  
    results = cursor.fetchall()	
    res=pickle.loads(results[0][3])    
    conn.close() 
    return(res)	


 
def kukoard(post_id,channel_id):
                    for i in range(0,len(add_post_array)):
                        if 	add_post_array[i].post_id==post_id:
                            mut=add_post_array[i].mut
                            pin=add_post_array[i].pin
                    if mut==0:
                        mut_str='⚪️ '
                    else:
                        mut_str='🔘 '
                    if pin==0:
                        pin_str='⚪️ '
                    else:
                        pin_str='🔘 '
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(types.InlineKeyboardButton(text='Добавить кнопки',callback_data=str(post_id)+'k'),
                    types.InlineKeyboardButton(text='Добавить реакцию',callback_data=str(post_id)+'r'),
                    types.InlineKeyboardButton(text='Опубликовать',callback_data=str(post_id)+'o'),
                    types.InlineKeyboardButton(text='Время публикации',callback_data=str(post_id)+'v'),
                    types.InlineKeyboardButton(text='Сохранить',callback_data=str(post_id)+'s'),
                    types.InlineKeyboardButton(text='Автоудаление',callback_data=str(post_id)+'d'),
                    types.InlineKeyboardButton(text='Предпросмотр',callback_data=str(post_id)+'p'),
                    types.InlineKeyboardButton(text='Начать сначала',callback_data=str(post_id)+'n'),
                    types.InlineKeyboardButton(text=pin_str+'Закрепить',callback_data=str(post_id)+'z'),
                    types.InlineKeyboardButton(text=mut_str+'Уведомления',callback_data=str(post_id)+'u'),
                    types.InlineKeyboardButton(text='Удалить пост',callback_data=str(post_id)+'l'),
                    types.InlineKeyboardButton(text='Вернуться к каналу',callback_data=str(channel_id)+'!'))
                    return(keyboard)
############################################# dostaem photo dla posta	
@bot.message_handler(content_types=['photo'])
def photoget(message):
    print(message)
    ll=1
    if message.chat.id in add_post:
        add_post.remove(message.chat.id)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==message.chat.id:
                add_post_array[i].document_type='photo'
                add_post_array[i].text=message.caption
                print(message.text)
                add_post_array[i].document=str(add_post_array[i].post_id)+'.jpg'
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id
                fileid=(message.photo[2].file_id)
                bb=bot.get_file(fileid)
                bb=bb.file_path
                logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
                f = open("documents/"+add_post_array[i].document, "wb")
                f.write(logo)
                f.close()
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(types.InlineKeyboardButton(text='Добавить кнопки',callback_data=str(post_id)+'k'),
                types.InlineKeyboardButton(text='Добавить реакцию',callback_data=str(post_id)+'r'),
                types.InlineKeyboardButton(text='Опубликовать',callback_data=str(post_id)+'o'),
                types.InlineKeyboardButton(text='Время публикации',callback_data=str(post_id)+'v'),
                types.InlineKeyboardButton(text='Сохранить',callback_data=str(post_id)+'s'),
                types.InlineKeyboardButton(text='Автоудаление',callback_data=str(post_id)+'d'),
                types.InlineKeyboardButton(text='Предпросмотр',callback_data=str(post_id)+'p'),
                types.InlineKeyboardButton(text='Начать сначала',callback_data=str(post_id)+'n'),
                types.InlineKeyboardButton(text='⚪️ Закрепить',callback_data=str(post_id)+'z'),
                types.InlineKeyboardButton(text='⚪️ Уведомления',callback_data=str(post_id)+'u'),
                types.InlineKeyboardButton(text='Удалить пост',callback_data=str(post_id)+'l'),
                types.InlineKeyboardButton(text='Вернуться к каналу',callback_data=str(channel_id)+'!'))
                msg =bot.send_message(message.chat.id, lengstr(ll,13),reply_markup=keyboard) 
########################### dostaem audio	
@bot.message_handler(content_types=['audio'])
def photoget(message):
    print(message)
    ll=1
    if message.chat.id in add_post:
        msg =bot.send_message(message.chat.id, lengstr(ll,20))
        add_post.remove(message.chat.id)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==message.chat.id:
                add_post_array[i].document_type='audio'
                add_post_array[i].text=message.caption
                print(message.text)
                add_post_array[i].document=str(add_post_array[i].post_id)+'.mp3'
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id
                fileid=(message.audio.file_id)
                bb=bot.get_file(fileid)
                bb=bb.file_path
                logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
                f = open("documents/"+add_post_array[i].document, "wb")
                f.write(logo)
                f.close()
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(types.InlineKeyboardButton(text='Добавить кнопки',callback_data=str(post_id)+'k'),
                types.InlineKeyboardButton(text='Добавить реакцию',callback_data=str(post_id)+'r'),
                types.InlineKeyboardButton(text='Опубликовать',callback_data=str(post_id)+'o'),
                types.InlineKeyboardButton(text='Время публикации',callback_data=str(post_id)+'v'),
                types.InlineKeyboardButton(text='Сохранить',callback_data=str(post_id)+'s'),
                types.InlineKeyboardButton(text='Автоудаление',callback_data=str(post_id)+'d'),
                types.InlineKeyboardButton(text='Предпросмотр',callback_data=str(post_id)+'p'),
                types.InlineKeyboardButton(text='Начать сначала',callback_data=str(post_id)+'n'),
                types.InlineKeyboardButton(text='⚪️ Закрепить',callback_data=str(post_id)+'z'),
                types.InlineKeyboardButton(text='⚪️ Уведомления',callback_data=str(post_id)+'u'),
                types.InlineKeyboardButton(text='Удалить пост',callback_data=str(post_id)+'l'),
                types.InlineKeyboardButton(text='Вернуться к каналу',callback_data=str(channel_id)+'!'))
                msg =bot.send_message(message.chat.id, lengstr(ll,13),reply_markup=keyboard)
####################### dostaem video
@bot.message_handler(content_types=['video'])
def photoget(message):
    print(message)
    ll=1
    if message.chat.id in add_post:
        msg =bot.send_message(message.chat.id, lengstr(ll,20))
        add_post.remove(message.chat.id)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==message.chat.id:
                add_post_array[i].document_type='video'
                add_post_array[i].text=message.caption
                print(message.text)
                add_post_array[i].document=str(add_post_array[i].post_id)+'.mp4'
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id
                fileid=(message.video.file_id)
                bb=bot.get_file(fileid)
                bb=bb.file_path
                logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
                f = open("documents/"+add_post_array[i].document, "wb")
                f.write(logo)
                f.close()
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(types.InlineKeyboardButton(text='Добавить кнопки',callback_data=str(post_id)+'k'),
                types.InlineKeyboardButton(text='Добавить реакцию',callback_data=str(post_id)+'r'),
                types.InlineKeyboardButton(text='Опубликовать',callback_data=str(post_id)+'o'),
                types.InlineKeyboardButton(text='Время публикации',callback_data=str(post_id)+'v'),
                types.InlineKeyboardButton(text='Сохранить',callback_data=str(post_id)+'s'),
                types.InlineKeyboardButton(text='Автоудаление',callback_data=str(post_id)+'d'),
                types.InlineKeyboardButton(text='Предпросмотр',callback_data=str(post_id)+'p'),
                types.InlineKeyboardButton(text='Начать сначала',callback_data=str(post_id)+'n'),
                types.InlineKeyboardButton(text='⚪️ Закрепить',callback_data=str(post_id)+'z'),
                types.InlineKeyboardButton(text='⚪️ Уведомления',callback_data=str(post_id)+'u'),
                types.InlineKeyboardButton(text='Удалить пост',callback_data=str(post_id)+'l'),
                types.InlineKeyboardButton(text='Вернуться к каналу',callback_data=str(channel_id)+'!'))
                msg =bot.send_message(message.chat.id, lengstr(ll,13),reply_markup=keyboard)
######################### dostaem document
@bot.message_handler(content_types=['document'])
def photoget(message):
    print(message)
    ll=1
    if message.chat.id in add_post:
        msg =bot.send_message(message.chat.id, lengstr(ll,20))
        add_post.remove(message.chat.id)
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].user_id==message.chat.id:
                add_post_array[i].document_type='document'
                add_post_array[i].text=message.caption
                print(message.text)
                file_get_ex=''
                for z in range(0,len(message.document.file_name)):
                    if message.document.file_name[z]=='.':
                        file_get_ex=message.document.file_name[z:]
                add_post_array[i].document=str(add_post_array[i].post_id)+file_get_ex
                post_id=add_post_array[i].post_id
                channel_id=add_post_array[i].channel_id
                fileid=(message.document.file_id)
                bb=bot.get_file(fileid)
                bb=bb.file_path
                logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
                f = open("documents/"+add_post_array[i].document, "wb")
                f.write(logo)
                f.close()
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(types.InlineKeyboardButton(text='Добавить кнопки',callback_data=str(post_id)+'k'),
                types.InlineKeyboardButton(text='Добавить реакцию',callback_data=str(post_id)+'r'),
                types.InlineKeyboardButton(text='Опубликовать',callback_data=str(post_id)+'o'),
                types.InlineKeyboardButton(text='Время публикации',callback_data=str(post_id)+'v'),
                types.InlineKeyboardButton(text='Сохранить',callback_data=str(post_id)+'s'),
                types.InlineKeyboardButton(text='Автоудаление',callback_data=str(post_id)+'d'),
                types.InlineKeyboardButton(text='Предпросмотр',callback_data=str(post_id)+'p'),
                types.InlineKeyboardButton(text='Начать сначала',callback_data=str(post_id)+'n'),
                types.InlineKeyboardButton(text='⚪️ Закрепить',callback_data=str(post_id)+'z'),
                types.InlineKeyboardButton(text='⚪️ Уведомления',callback_data=str(post_id)+'u'),
                types.InlineKeyboardButton(text='Удалить пост',callback_data=str(post_id)+'l'),
                types.InlineKeyboardButton(text='Вернуться к каналу',callback_data=str(channel_id)+'!'))
                msg =bot.send_message(message.chat.id, lengstr(ll,13),reply_markup=keyboard)

def deleterer():
    conn = sqlite3.connect('Thread.sqlite')
    cursor = conn.cursor()
	
    array=[]
    now_time=int(time.time())
    cursor.execute("SELECT * FROM DELETER WHERE DELETE_TIME <= :time",{"time":now_time})
    results = cursor.fetchall()	
    print(results)
    cursor.execute("DELETE FROM DELETER WHERE DELETE_TIME <= :time",{"time":now_time})
    conn.commit()    
    conn.close()
    for i in range(0,len(results)):
        msg=bot.delete_message(results[i][1],results[i][0])	
        
def forserer():
    conn = sqlite3.connect('Thread.sqlite')
    cursor = conn.cursor()
	
    array=[]
    now_time=int(time.time())
    cursor.execute("SELECT * FROM FORSEDER WHERE FORSE_TIME <= :time",{"time":now_time})
    results = cursor.fetchall()	
    print(results)
    cursor.execute("DELETE FROM FORSEDER WHERE FORSE_TIME <= :time",{"time":now_time})
    conn.commit()    
    conn.close()
    for i in range(0,len(results)):
        obj=pickle.loads(results[i][1]) 
        keyboard = types.InlineKeyboardMarkup()
        for z in range(0,len(obj.buttons_url)):
            print(obj.buttons[z],obj.buttons_url[z])
            url_button = types.InlineKeyboardButton(text=obj.buttons[z], url=obj.buttons_url[z])
            keyboard.add(url_button)
        if len(obj.reactions)>0:
            keyboard.add(*[types.InlineKeyboardButton(text=name+':0',callback_data='roact'+str(obj.reactions.index(name))+':'+name) for name in add_post_array[i].reactions])
            			
        if 	obj.mut==1:
            mut=True
        else:
            mut=False	
        if 	obj.document_type=='':				
            msg =bot.send_message(obj.channel_id, obj.text,reply_markup=keyboard,disable_notification=mut)
        if  obj.document_type=='photo':
            msg =bot.send_photo(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)                    
        if  obj.document_type=='audio':
            msg =bot.send_audio(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)
        if  obj.document_type=='video':
            msg =bot.send_video(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)
        if  obj.document_type=='document':
            msg =bot.send_document(obj.channel_id, open('documents/'+obj.document, 'rb'),caption=obj.text,reply_markup=keyboard,disable_notification=mut)
   
        joy=msg.message_id
        if len(obj.reactions)>0:
            add_reactions(obj.channel_id,joy,obj.reactions)
        if obj.delete_time>0:
            add_delete_func(joy,obj.channel_id,obj.delete_time)                
        if 	obj.pin==1:
            msg=bot.pin_chat_message(obj.channel_id,joy,disable_notification=mut)
        if obj.saved==0:
                    os.remove("documents/"+obj.document)			
                	
        



schedule.every(1).minutes.do(deleterer)
schedule.every(1).minutes.do(forserer)
def lal():
    while 1:
        schedule.run_pending()
        time.sleep(1)
_thread.start_new_thread(lal,())					
	
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