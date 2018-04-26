import openpyxl
import time
import telebot
import sqlite3
from telebot import types



wb = openpyxl.load_workbook(filename = 'leng.xlsx')
sheet = wb['test']
val = sheet.cell(row=1, column=1)
print(val.value)
def  lengstr(leng,strn):
    bb=sheet.cell(row=strn, column=leng).value
    return str(bb)
API_TOKEN = '500239333:AAEpjOsc00JC1_2cw_Kaq_--VIdv_QzSMTA'

class post():
    user_id=0
    channel_id=0
    text=''
    document=''
    document_type=''
    post_id=0	


bot = telebot.TeleBot(API_TOKEN)
global add_channel, add_post, add_post_array,posts
posts=0
add_channel=[]
add_post=[]
add_post_array=[]
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
    global add_channel, add_post, add_post_array, posts
    ll=1
################################## Kanal 
    if c.data[-1]=='$':
        channel_id=c.data[:-1]
        channel_name=chan_name_func(channel_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'%') for name in ['Создать публикацию']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'@') for name in ['Мои публикации']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'&') for name in ['Автопостинг']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'*') for name in ['Настройки']])
        msg =bot.send_message(c.message.chat.id, channel_name,reply_markup=keyboard)
        return		
################################# vse kanali
    if c.data =='Все каналы':
        channel_id=c.data[:-1]
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
        add_post_array[-1].user_id=c.message.chat.id
        add_post_array[-1].channel_id=int(c.data[:-1])
        add_post_array[-1].post_id=int(posts) 
        posts+=1
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
                del add_post_array[i]
        channel_id=c.data[:-1]
        channel_name=chan_name_func(channel_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'%') for name in ['Создать публикацию']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'@') for name in ['Мои публикации']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'&') for name in ['Автопостинг']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=str(channel_id)+'*') for name in ['Настройки']])
        msg =bot.send_message(c.message.chat.id, channel_name,reply_markup=keyboard)  
        return
    if c.data[-1]=='o':
        for i in range(0,len(add_post_array)):
            if 	add_post_array[i].post_id==int(c.data[:-1]):
                msg =bot.send_message(add_post_array[i].channel_id, add_post_array[i].text)
                msg =bot.answer_callback_query(c.id,lengstr(ll,14)) 
                return				
    msg =bot.answer_callback_query(c.id,'Эта функция пока не доступна')     				
    return		
		
		
		
		
		
def name(m):
    global add_channel, add_post, add_post_array, posts
    ll=1
#####################   Dobavlenie kanala
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
        types.InlineKeyboardButton(text='Удалить',callback_data=str(post_id)+'d'),
        types.InlineKeyboardButton(text='Предпросмотр',callback_data=str(post_id)+'p'),
        types.InlineKeyboardButton(text='Начать сначала',callback_data=str(post_id)+'n'),
        types.InlineKeyboardButton(text='🔘 Закрепить',callback_data=str(post_id)+'z'),
        types.InlineKeyboardButton(text='🔘 Уведомления',callback_data=str(post_id)+'u'),
        types.InlineKeyboardButton(text='Вернуться к каналу',callback_data=str(channel_id)+'!'))
        msg =bot.send_message(m.chat.id, lengstr(ll,13),reply_markup=keyboard)        				
			
			
			
			
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
    cursor.execute("SELECT * FROM USERS WHERE USER LIKE :user_id",{"user_id":user_id})
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
	
    cursor.execute("SELECT TITLE FROM USERS WHERE CHANNEL LIKE :channel_id",{"channel_id":channel_id})
    results = cursor.fetchall()
    print(results)
    return(results)



	
if __name__ == '__main__':

            bot.polling(none_stop=True)