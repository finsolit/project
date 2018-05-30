import telebot
import time
import threading
import datetime
import copy
from datetime import datetime
import schedule
from telebot import types
import _pickle as pickle
import os
import _thread
import urllib
import sqlite3
import openpyxl
global inadmin, password, admin_id, oprcall, oprs, add_opr, work_with_opr, add_vopros_admin, filter,txtrassilki
add_vopros_admin=0
oprcall=1
add_opr=0
inadmin=[]
filter=[]
txtrassilki=''
password='qwe123'
input = open('admin.pkl', 'rb')
admin_id = pickle.load(input)
input.close()
input = open('oprs.pkl', 'rb')
oprs = pickle.load(input)
input.close()
print(admin_id)
wb = openpyxl.load_workbook(filename = 'leng.xlsx')
sheet = wb['test']
val = sheet.cell(row=1, column=1)
print(val.value)
def  lengstr(leng,strn):
    bb=sheet.cell(row=strn, column=leng).value
    return str(bb)
TOKEN = '610139121:AAGVi9j83DjZ-RI7rvEeAEt4H4R5Lp31hKA'
WEBHOOK_HOST = '95.46.98.126'
WEBHOOK_PORT = 80  # 443, 80, 88 или 8443 (порт должен быть открыт!)
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

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text=lengstr(1,3),callback_data='%'),
                     types.InlineKeyboardButton(text=lengstr(1,4),callback_data='@'))
    msg = bot.send_message(message.chat.id, lengstr(1,2),reply_markup=keyboard)

	
	
@bot.message_handler(commands=['admin'])	
def admin(m):
    inadmin.append(m.chat.id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text=lengstr(1,11),callback_data='!'))
    msg = bot.send_message(m.chat.id, lengstr(1,10),reply_markup=keyboard)    
    return()	
	
	

	
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    name(message)	
	
	
	
@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    global oprs, add_opr, work_with_opr, add_vopros_admin, filter,txtrassilki
    bib=c.message.message_id
    if 'otv' in c.data:
        print(c.data)
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                lst=i+1
                otvet_id=c.data[3:i]
            if c.data[i]=='†':
                opr_id=c.data[lst:i]
                vopros_id=c.data[i+1:]
        add_otvet_in(c.message.chat.id,opr_id,vopros_id,otvet_id)
        print(c.message.chat.id,opr_id,vopros_id,otvet_id)
        chek_next_question(c.message.chat.id,bib,opr_id,vopros_id)
        return
    if c.data=='!':
        inadmin.remove(c.message.chat.id)
        msg = bot.send_message(c.message.chat.id, lengstr(1,14))   
        return		
    if c.data=='%':
        add_urist(c.message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [lengstr(1,6)]])
        msg = bot.send_message(c.message.chat.id, lengstr(1,5),reply_markup=keyboard) 
        return		
    if c.data=='@':
        add_client(c.message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [lengstr(1,8),lengstr(1,9)]])
        msg = bot.send_message(c.message.chat.id, lengstr(1,7),reply_markup=keyboard) 
        return
    if c.data=='addopr':
        oprs+=1
        output = open('oprs.pkl', 'wb')
        pickle.dump(oprs, output, 2)
        output.close()	
        add_opr=1
        msg = bot.send_message(c.message.chat.id, lengstr(1,20))  
        return
    if c.data=='extxt':
        msg = bot.send_message(c.message.chat.id, lengstr(1,41))   
        txtrassilki=''		
        return
######################## Vvod teksta rassilki
    if c.data=='txtras':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='extxt') for name in [lengstr(1,40)]])
        msg = bot.send_message(c.message.chat.id, lengstr(1,39),reply_markup=keyboard)   
        txtrassilki=1		
        return
################################################
    if 'ddelopr' in c.data:
            opr_id=int(c.data[:-7])	 
            delete_opros(opr_id)
            dsa=all_oprosi()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in range(0,len(dsa)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='cop'+str(dsa[i][0])) for name in [dsa[i][1]]]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addopr') for name in [lengstr(1,19)]])                 
            msg = bot.send_message(c.message.chat.id, lengstr(1,18)+' '+str(len(dsa)),reply_markup=keyboard) 
            return()			
    if 'delopr' in c.data:
        opr_id=int(c.data[:-6])	
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Нет',callback_data='cop'+str(opr_id)),
                    types.InlineKeyboardButton(text='Да',callback_data=str(opr_id)+'ddelopr'))
        msg = bot.send_message(c.message.chat.id, lengstr(1,24),reply_markup=keyboard)
        return
    if 'addvopr' in c.data:
        opr_id=int(c.data[:-7])	
        add_vopros_admin=1
        work_with_opr=opr_id
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='Отмена',callback_data='cop'+str(opr_id)))
        msg = bot.send_message(c.message.chat.id, lengstr(1,25),reply_markup=keyboard)
        return
    if 'razoslat' in c.data:
        opr_id=int(c.data[:-8])	
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Нет',callback_data='cop'+str(opr_id)),
                    types.InlineKeyboardButton(text='Да',callback_data=str(opr_id)+'razuslat'))
        msg = bot.send_message(c.message.chat.id, lengstr(1,32),reply_markup=keyboard)
        return    
    if 'razuslat' in c.data:
        opr_id=int(c.data[:-8])	
        rassilka_oprosa(opr_id)	
        msg = bot.send_message(c.message.chat.id, lengstr(1,29))
    if 'delvopr' in c.data:
        opr_id=int(c.data[:-7])
        zz=''		
        spisok=spisok_voprosov(opr_id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(len(spisok)):
            zz+=str(i+1)+') '+spisok[i][0]+'\n'
            keyboard.add(types.InlineKeyboardButton(text=str(i+1),callback_data='dzx'+str(i)+':'+str(opr_id)))             
        keyboard.add(types.InlineKeyboardButton(text='Отмена',callback_data='cop'+str(opr_id)))
        msg = bot.send_message(c.message.chat.id, lengstr(1,27)+'\n\n'+zz,reply_markup=keyboard) 
        return		
    if 'dzx' in c.data:
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                num=c.data[3:i]
                opr_id=c.data[i+1:]
        delete_vopros(num,opr_id)
        msg = bot.send_message(c.message.chat.id, lengstr(1,28))	
        return		
    if 'cop' in c.data:
        opr_id=int(c.data[3:])
        zz='Error'
        add_vopros_admin=0
        zz=chek_opros_full(opr_id)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Удалить вопрос',callback_data=str(opr_id)+'delvopr'),
                    types.InlineKeyboardButton(text='Добавить вопрос',callback_data=str(opr_id)+'addvopr'),
                    types.InlineKeyboardButton(text='Удалить опрос',callback_data=str(opr_id)+'delopr'),
                    types.InlineKeyboardButton(text='Разослать опрос',callback_data=str(opr_id)+'razoslat'))
        msg = bot.send_message(c.message.chat.id, zz,reply_markup=keyboard) 
        return		
    if 'stt' in c.data:
        opr_id=int(c.data[3:])
        zz='Error'
        zz=stat_opros(opr_id)
        msg = bot.send_message(c.message.chat.id, zz) 
        return	
############################### sozdanie filtra
    if 'ras' in c.data:
        opr_id=int(c.data[3:])
        work_with_opr=opr_id
        kr=chek_op(opr_id)
        if kr==1:
           zz=lengstr(1,37)
        else:
           zz=lengstr(1,36)
           msg = bot.send_message(c.message.chat.id, zz) 
           return	
        create_filter(opr_id)
        keyboard=keyboard_for_filter(opr_id)
                        
        msg = bot.send_message(c.message.chat.id, zz,reply_markup=keyboard) 
        return	
    if 'ifm' in c.data:
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                su=int(c.data[3:i])
                tt=i+1
            if c.data[i]=='†':
                zu=int(c.data[tt:i])
                opr_id=int(c.data[i+1:])         	
        if filter[su][zu]==1:
           filter[su][zu]=0
        else:
           filter[su][zu]=1	
        print(filter)
        keyboard=keyboard_for_filter(opr_id)
        msg = bot.edit_message_reply_markup(c.message.chat.id, bib,reply_markup=keyboard) 
        return		
    return()		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
def name(m):
    global admin_id, add_opr, oprs, work_with_opr, add_vopros_admin, filter,txtrassilki
    if m.chat.id in inadmin:
        if m.text==password:
            admin_id=m.chat.id
            output = open('admin.pkl', 'wb')
            pickle.dump(admin_id, output, 2)
            output.close()
            inadmin.remove(m.chat.id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [lengstr(1,15),lengstr(1,16),lengstr(1,17),lengstr(1,33),lengstr(1,42)]])
            msg = bot.send_message(m.chat.id, lengstr(1,12),reply_markup=keyboard)  
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(types.InlineKeyboardButton(text=lengstr(1,11),callback_data='!'))
            msg = bot.send_message(m.chat.id, lengstr(1,13),reply_markup=keyboard) 
 
    if add_vopros_admin==1 and m.chat.id==admin_id:
        zxvopros=m.text
        for i in range(0,len(zxvopros)):
            if zxvopros[i]=='\n':
                vopros=zxvopros[:i]
                stroka=zxvopros[i+1:]+'\n'
                break
        otvet=[]
        last=0
        for i in range(1,len(stroka)):
            if stroka[i]=='\n':
                otvet.append(stroka[last:i])
                last=i+1
        otvet=pickle.dumps(otvet)
        add_vopros_opt(vopros,otvet,work_with_opr)       
        add_vopros_admin=0
        opr_id=work_with_opr
        zz='Error'
        zz=chek_opros_full(opr_id)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Удалить вопрос',callback_data=str(opr_id)+'delvopr'),
                    types.InlineKeyboardButton(text='Добавить вопрос',callback_data=str(opr_id)+'addvopr'),
                    types.InlineKeyboardButton(text='Удалить опрос',callback_data=str(opr_id)+'delopr'),
                    types.InlineKeyboardButton(text='Разослать опрос',callback_data=str(opr_id)+'razoslat'))
        msg = bot.send_message(m.chat.id, zz,reply_markup=keyboard) 
        return
######################### rassilka texta po filtram oprosa
    if txtrassilki==1:
        txtrassilki=m.text
        print(filter,txtrassilki,work_with_opr)
        rassilka_po_filtru(m.text,work_with_opr)
        txtrassilki=''

#######################
 
    if add_opr==1 and m.chat.id==admin_id:
        add_opr_in_db(m.text,oprs)
        work_with_opr=oprs
        add_opr=2
        msg = bot.send_message(m.chat.id, lengstr(1,21))   
        return
    if add_opr==2 and m.chat.id==admin_id:
        add_vopros(m.text,work_with_opr)
        add_opr=3
        msg = bot.send_message(m.chat.id, lengstr(1,22)) 
        return	
    if add_opr==3 and m.chat.id==admin_id:
        otvet=[]
        stroka=m.text+'\n'
        last=0
        for i in range(1,len(stroka)):
            if stroka[i]=='\n':
                otvet.append(stroka[last:i])
                last=i+1
        otvet=pickle.dumps(otvet)
        add_otvet(otvet,work_with_opr)
        add_opr=0
        msg = bot.send_message(m.chat.id, lengstr(1,23)) 
        return			
    if lengstr(1,15)==m.text and m.chat.id==admin_id:
            dsa=all_oprosi()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in range(0,len(dsa)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='cop'+str(dsa[i][0])) for name in [dsa[i][1]]]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addopr') for name in [lengstr(1,19)]])                 
            msg = bot.send_message(m.chat.id, lengstr(1,18)+' '+str(len(dsa)),reply_markup=keyboard)      
    if lengstr(1,33)==m.text and m.chat.id==admin_id:
            dsa=all_oprosi()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in range(0,len(dsa)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='stt'+str(dsa[i][0])) for name in [dsa[i][1]]])                 
            msg = bot.send_message(m.chat.id, lengstr(1,35),reply_markup=keyboard) 	
    if lengstr(1,16)==m.text and m.chat.id==admin_id:
            dsa=all_oprosi()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in range(0,len(dsa)):
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='ras'+str(dsa[i][0])) for name in [dsa[i][1]]])                 
            msg = bot.send_message(m.chat.id, lengstr(1,34),reply_markup=keyboard) 			
    return

def all_oprosi():
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OPROSI")
    results = cursor.fetchall()
    conn.close()
    print(results)
    return(results)   

def add_urist(user_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("insert into USERS_UR values (:post_id) ", {"post_id": user_id})
    conn.commit()
    conn.close()
	
def add_opr_in_db(name,id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("insert into OPROSI values (:post_id, :name) ", {"post_id": id,"name": name})
    conn.commit()
    conn.close()	

	
def add_vopros(vopros,id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("insert into VOPROSI values (:post_id, :name, :otvet) ", {"post_id": id,"name": vopros,"otvet": ''})
    conn.commit()
    conn.close()
	
def add_otvet(vopros,id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE VOPROSI SET OTVETI = :name WHERE OPROS_ID = :id ", {"name": vopros,"id": id})
    conn.commit()
    conn.close()	

def  add_vopros_opt(vopros,otvet,id) :
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("insert into VOPROSI values (:post_id, :name, :otvet) ", {"post_id": id,"name": vopros,"otvet": otvet})
    conn.commit()
    conn.close()

	
def add_client(user_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("insert into USERS_CL values (:post_id) ", {"post_id": user_id})
    conn.commit()
    conn.close()

	
def chek_opros_full(id):
    res='Название опроса: '
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT NAME FROM OPROSI WHERE ID=:id", {"id": id})
    results = cursor.fetchall()
    conn.close()  
    print(results)
    res+=results[0][0]+'\n'
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT TEXT FROM VOPROSI WHERE OPROS_ID=:id", {"id": id})
    results1 = cursor.fetchall()
    cursor.execute("SELECT OTVETI FROM VOPROSI WHERE OPROS_ID=:id", {"id": id})
    results2 = cursor.fetchall()
    conn.close()    
    for i in range(0,len(results1)):
        res+='\nВопрос №'+str(i+1)+' : '+results1[i][0]+'\nВарианты ответов:\n'
        otveti=pickle.loads(results2[i][0])
        for k in range(0,len(otveti)):
                res+=otveti[k]+'\n'
    return(res)			
	
def delete_opros(id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM OPROSI WHERE ID=:id", {"id": id})
    conn.commit()
    conn.close()  
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM VOPROSI WHERE OPROS_ID=:id", {"id": id})
    conn.commit()
    conn.close()    
    return()	
	
	
	
	
def spisok_voprosov(id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT TEXT FROM VOPROSI WHERE OPROS_ID = :id", {"id": id})
    results = cursor.fetchall()
    conn.close()
    return(results)    

def   delete_vopros(num,opr_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT TEXT FROM VOPROSI WHERE OPROS_ID = :id", {"id": opr_id})
    results = cursor.fetchall()
    conn.close()
    tt=results[int(num)][0]
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM VOPROSI WHERE TEXT=:id", {"id": tt})
    conn.commit()
    conn.close()         





def  rassilka_oprosa(opr_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT TEXT FROM VOPROSI WHERE OPROS_ID = :id", {"id": opr_id})
    results = cursor.fetchall()
    conn.close()
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    aa=[]
    aa=pickle.dumps(aa)
    for i in range(0,len(results)):
        cursor.execute("insert into OTVETI values (:post_id, :name, :otvet, :otvet1) ", {"post_id": opr_id,"name": i,"otvet": aa, "otvet1": aa})
        conn.commit()
    conn.close()
    t = threading.Thread(target=clock, args=(opr_id,))
    t.start()




	
def clock(opr_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USERS_CL")
    results = cursor.fetchall()
    conn.close()    
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VOPROSI WHERE OPROS_ID = :id", {"id": opr_id})
    results1 = cursor.fetchall()
    conn.close()    
    for i in range(0,len(results)):
        if i % 15==0:
            time.sleep(1)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        otveti=pickle.loads(results1[i][2])  
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otv'+str(otveti.index(name))+':'+str(opr_id)+'†'+str(0)) for name in otveti])            		
        msg=bot.send_message(results[i][0],lengstr(1,30)+'\n\n'+results1[0][1],reply_markup=keyboard)



def add_otvet_in(user_id,opr_id,vopros_id,otvet_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OTVETI WHERE OPROS_ID = :opr_id and VOPROS_ID = :vopros_id", {"opr_id": opr_id,"vopros_id": vopros_id})
    results = cursor.fetchall()
    conn.close()
    users=pickle.loads(results[0][2])
    print(users)
    otveti=pickle.loads(results[0][3])	
    print(otveti)
    users.append(user_id)
    otveti.append(otvet_id)
    users=pickle.dumps(users)
    otveti=pickle.dumps(otveti)
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE OTVETI SET USERS=:users WHERE OPROS_ID = :opr_id and VOPROS_ID = :vopros_id ", {"users": users,"opr_id": opr_id,"vopros_id": vopros_id})
    cursor.execute("UPDATE OTVETI SET ANSW=:otveti WHERE OPROS_ID = :opr_id and VOPROS_ID = :vopros_id ", {"otveti": otveti,"opr_id": opr_id,"vopros_id": vopros_id})
    conn.commit()
    conn.close()    

	
	
def   chek_next_question(user_id,bib,opr_id,vopros_id):    
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    vopros_id=int(vopros_id)
    cursor.execute("SELECT * FROM VOPROSI WHERE OPROS_ID = :id", {"id": opr_id})
    results1 = cursor.fetchall()
    conn.close()  
    vopros_id+=1
    if len(results1)==vopros_id:
           msg = bot.edit_message_text(chat_id=user_id, message_id=bib, text=lengstr(1,31)) 	
           return
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    otveti=pickle.loads(results1[vopros_id][2])  
    keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otv'+str(otveti.index(name))+':'+str(opr_id)+'†'+str(vopros_id)) for name in otveti])            		
    msg=bot.edit_message_text(chat_id=user_id, message_id=bib,text=results1[vopros_id][1],reply_markup=keyboard)
	
	
	
def stat_opros(opr_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OTVETI WHERE OPROS_ID = :opr_id", {"opr_id": opr_id})
    results1 = cursor.fetchall()
    conn.close()
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VOPROSI WHERE OPROS_ID = :id", {"id": opr_id})
    results2 = cursor.fetchall()
    conn.close()
    res=''
    if len(results1)==0:
        res=lengstr(1,36)
        return(res)
    for i in range(0,len(results2)):
            col_vo=len(pickle.loads(results1[i][3]))
            otv=pickle.loads(results1[i][3])
            res+='Вопрос №'+str(i+1)+'\n'+results2[i][1]+'\nВсего ответило: '+str(col_vo)+'\n\n'
            col_ot=len(pickle.loads(results2[i][2]))
            var_ot=pickle.loads(results2[i][2])
            for k in range(0,col_ot):
                sum=0
                for j in range(0,col_vo):
                    if str(otv[j])==str(k):
                        sum+=1
                res+=var_ot[k]+' - '+str(sum)+'\n'
            res+='\n'
    return(res)
  
def chek_op(opr_id):
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OTVETI WHERE OPROS_ID = :opr_id", {"opr_id": opr_id})
    results1 = cursor.fetchall()
    conn.close()
    if len(results1)==0:
        res=0
    else:
        res=1
    return(res)
  
  
  
  
def create_filter(opr_id):
    global filter
    filter=[]
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT TEXT FROM VOPROSI WHERE OPROS_ID=:id", {"id": opr_id})
    results1 = cursor.fetchall()
    cursor.execute("SELECT OTVETI FROM VOPROSI WHERE OPROS_ID=:id", {"id": opr_id})
    results2 = cursor.fetchall()
    conn.close()    
    for i in range(0,len(results1)):
        filter.append([])
        otveti=pickle.loads(results2[i][0])
        for k in range(0,len(otveti)):
                filter[-1].append(1)
    print(filter)	    
	
	
	
	
	
def keyboard_for_filter(opr_id):
    global filter	
    res=''

    fulter_emoji=copy.deepcopy(filter)
    for i in range(0,len(filter)):
        for k in range(0,len(filter[i])):
            if filter[i][k]==1:
                fulter_emoji[i][k]='✅'
            else:
                fulter_emoji[i][k]='❌'

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT TEXT FROM VOPROSI WHERE OPROS_ID=:id", {"id": opr_id})
    results1 = cursor.fetchall()
    cursor.execute("SELECT OTVETI FROM VOPROSI WHERE OPROS_ID=:id", {"id": opr_id})
    results2 = cursor.fetchall()
    conn.close() 

    for i in range(0,len(results1)):
        keyboard.add(types.InlineKeyboardButton(text='Вопрос №'+str(i+1),callback_data='„'))
        otveti=pickle.loads(results2[i][0])
        keyboard.add(*[types.InlineKeyboardButton(text=fulter_emoji[i][otveti.index(name)]+' '+name,callback_data='ifm'+str(i)+':'+str(otveti.index(name))+'†'+str(opr_id)) for name in otveti])
    keyboard.add(types.InlineKeyboardButton(text=lengstr(1,38),callback_data='txtras'))
    return(keyboard)	
	
	
def  rassilka_po_filtru(txt,opr_id):
    global filter	
    conn = sqlite3.connect('BD.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM OTVETI WHERE OPROS_ID = :opr_id", {"opr_id": opr_id})
    results = cursor.fetchall()
    conn.close()
    users_big=[]
    for i in range(0,len(filter)):
        spisokall=pickle.loads(results[i][2])
        for i in spisokall:
            users_big.append(i)
    users_big=list(set(users_big))
    for i in range(0,len(filter)):
        users_small=[]
        spisokall=pickle.loads(results[i][2])
        answersall=pickle.loads(results[i][3])
        for k in range(0,len(filter[i])):
            if filter[i][k]==0:
                continue
            else:
                for j in range(0,len(answersall)):
               	    if str(answersall[j])==str(k):
                        users_small.append(spisokall[j])	
        print(users_small)
        for m in range(0,len(users_big)):
            try:
             if users_big[m] in users_small:
                continue
             else:
                del users_big[m]
            except Exception:
             continue			
    print(users_big)
    t = threading.Thread(target=clock1, args=(txt,users_big))
    t.start()
        
      	
def clock1(txt,arr):
    for i in range(0,len(arr)):
        if i % 15==0:
            time.sleep(1)          		
        msg=bot.send_message(arr[i],txt)
	
	
	
	
	
	
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
