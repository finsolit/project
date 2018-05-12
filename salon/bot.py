import telebot
import time
import datetime
from datetime import datetime
import schedule
from telebot import types
import _pickle as pickle
import os
import _thread
import urllib
import cherrypy
TOKEN = '507631866:AAG6M_uboVpOF-FK4cpsLYgqBDtX4Rq2DvA'
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

arhiv_model=[]
arhiv_procedur=[]
arhiv_masterov=[]
arhiv_otzivov=[]
admin_addphoto=''
admin_password='QWERTY123456!@#$%^'
procedures=[]
kat_proc=[]
svazi=[]
input = open('armod.pkl', 'rb')
arhiv_model = pickle.load(input)
input.close()	
birthday_grac='Поздравляем вас с днем рождения!'
bith_change=0
input = open('arotz.pkl', 'rb')
arhiv_otzivov = pickle.load(input)
input.close()

rassilka=''
arhiv_photo=[]
input = open('arhiv_photo.pkl', 'rb')
arhiv_photo = pickle.load(input)
input.close()


input = open('arproc.pkl', 'rb')
arhiv_procedur = pickle.load(input)
input.close()

input = open('kat.pkl', 'rb')
kat_proc = pickle.load(input)
input.close()	
input = open('procedures.pkl', 'rb')
procedures = pickle.load(input)
input.close()	
	
input = open('armas.pkl', 'rb')
arhiv_masterov = pickle.load(input)
input.close()

input = open('bdpol.pkl', 'rb')
bdpol = pickle.load(input)
input.close()

class svaz():
    from_kat=0
    from_proc=0
    to_kat=0
    to_proc=0
new_svaz=''
class userobj():
    id=0
    name=''
    phone=0
    bithday=0	
    regpoz=0
    adminin=0
    model=0
    modelstr=''
    zakaz=0
    zakaz1=0
    predloj=['','']
    zakazstr=''
    otziv=''
    dopvar1=0
    dopvar2=0
    vopros=0
    dopvar3=0
    def __init__(self):
        self.predloj=['','']
global bdpol
admin=0
admin_addkat=0
admin_addproc=''
bdpol=[]
admin_username='lil'
admin_addmast=0
def nomer(b):
    global bdpol
    z=0
    k=-1
    for i in bdpol:
        k+=1
        if bdpol[k].id==b:
            z=k
            return(z)
			
				
			
input = open('svazi.pkl', 'rb')
svazi = pickle.load(input)
input.close()			
			
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
    if message.chat.id<0:
        return()
    global bdpol
    hesh=message.chat.id
    z=0
    k=-1
    for i in bdpol:
        k+=1
        if bdpol[k].id==hesh:
            z=1
    if z==0:
        bdpol.append(userobj())
        print(bdpol[-1].id)
        bdpol[-1].id=hesh
        bdpol[-1].start=1
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить контакт", request_contact=True)
        keyboard.add(button_phone)
        msg = bot.send_message(message.chat.id, '👩 Привет!\n'
        'Я - @cocopalmsalon, личный помощник салона красоты "Коко Пальм". Рад тебя приветствовать! \n'
        'Для авторизации нажми, пожалуйста,  кнопку "Отправить мой номер".',
        reply_markup=keyboard,parse_mode='HTML')
        return()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['F.A.Q.','Заказать процедуру']])
    keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Отзывы о работе мастеров','Портфолио']])
    keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Хочу быть моделью']])
    msg = bot.send_message(message.chat.id, 'Добро пожаловать в главное меню!',reply_markup=keyboard)

	
	
@bot.message_handler(commands=['admin'])	
def admin(m):
    global bdpol
    if m.chat.id>0:
        msg = bot.send_message(m.chat.id, 'Добро пожаловать в панель администратора!\n\nВведите, пожалуйста, пароль администратора.',parse_mode='HTML')
        k=nomer(m.chat.id)
        bdpol[k].adminin=1
    else:
        return()	
	
@bot.message_handler(commands=['deleteme'])	
def deleteme(m):
    global bdpol
    if m.chat.id>0:
        msg = bot.send_message(m.chat.id, 'Здравствуйте Дарья. Мы, команда разработки компании iBot. Мы больше не работаем с Артемом.\nЭта команда удалила вас из пользователей, нажмите /start что-бы пройти регистрацию вновь.',parse_mode='HTML')
        k=nomer(m.chat.id)
        del bdpol[k]
    else:
        return()	

	
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    name(message)	
	
	
	
@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    global bdpol, admin, admin_addkat, admin_addproc, svazi, new_svaz,arhiv_procedur, admin_addmast, admin_username,birthday_grac,bith_change, arhiv_photo, admin_addphoto
    bib=c.message.message_id
    if c.message.chat.id<0:
        return()
    k=nomer(c.message.chat.id)
###############################  zaprosi na model
    if c.data=='model1':
        bdpol[k].model=1
        bdpol[k].modelstr=bdpol[k].phone+' '+bdpol[k].name+' '
        msg = bot.send_message(c.message.chat.id,'Укажите,  пожалуйста длину Ваших волос.')
    if c.data=='model2':
        bdpol[k].model=6
        bdpol[k].modelstr=bdpol[k].phone+' '
        msg = bot.send_message(c.message.chat.id,'Укажите,  пожалуйста длину Ваших волос.')
    if c.data=='model3':
        bdpol[k].model=8
        bdpol[k].modelstr=bdpol[k].phone+' '
        msg = bot.send_message(c.message.chat.id,'Укажите, пожалуйста Ваш возраст.')
############################# prosmotr modelei v arhive
    if 'armod:' in c.data:
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        msg = bot.delete_message(c.message.chat.id, bib)		
        if zp==len(arhiv_model)-1:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='armod:'+str(zp-1)) for name in ['➡']]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='demod:'+str(len(arhiv_model)-2)) for name in ['Удалить']])
        elif zp==0:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='armod:'+str(zp+1)) for name in ['⬅️']])  
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='demod:'+str(len(arhiv_model)-2)) for name in ['Удалить']])	
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='armod:'+str(zp-1)) for name in ['➡']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='armod:'+str(zp+1)) for name in ['⬅️']]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='demod:'+str(zp)) for name in ['Удалить']])				
        if arhiv_model[zp][-1]=='$':
            print('ok eto photo')
            for i in range(1,len(arhiv_model[zp])-1) :
                zk=(i+1)*-1	
                if 	arhiv_model[zp][zk]==':':
                    photka=arhiv_model[zp][zk+1:-1]
                    print(photka)					
                    msg = bot.send_photo(c.message.chat.id, photo=open('models/'+str(photka)+'.jpg', 'rb'),caption=arhiv_model[zp],reply_markup=keyboard)  
                    break
        else:
            msg = bot.send_message(c.message.chat.id, arhiv_model[zp],reply_markup=keyboard)    
######################## Udalenie iz arhiva modelei
    if 'demod:' in c.data:	
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        del arhiv_model[zp]
        msg = bot.delete_message(c.message.chat.id, bib)
        msg = bot.send_message(c.message.chat.id, 'Запись удалена')	
########################## Prosmotr portfolio foto
    if c.data[0]=='$':
        papka=c.data[1:5]
        nomers=c.data[5:]
        print(nomers)
        if papka == 'make':
           ss=0
           max=len(arhiv_photo[0])
        if papka == 'nogt':
           ss=1
           max=len(arhiv_photo[1])
        if papka == 'okra':
           ss=2
           max=len(arhiv_photo[2])
        if papka == 'tatj':
           ss=3
           max=len(arhiv_photo[3])
        if papka == 'tatu':
           ss=4
           max=len(arhiv_photo[4])
        if papka == 'zubi':
           ss=5
           max=len(arhiv_photo[5])
        if int(nomers)>=max:
            nomers=str(0)		   
        if int(nomers) <0:
            nomers=str(max-1)				
        mnomer=str(int(nomers)-1)	
        pnomer=str(int(nomers)+1)		
        msg = bot.delete_message(c.message.chat.id, bib)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='⬅️',callback_data='$'+papka+mnomer),types.InlineKeyboardButton(text='➡',callback_data='$'+papka+pnomer))   
        msg = bot.send_photo(c.message.chat.id, photo=open(papka+'/'+arhiv_photo[ss][int(nomers)], 'rb'),reply_markup=keyboard) 
############################# portfolio admina
    if c.data[0]=='^':
        papka=c.data[1:5]
        nomers=c.data[5:]
        print(nomers)
        if papka == 'make':
           ss=0
           max=len(arhiv_photo[0])
        if papka == 'nogt':
           ss=1
           max=len(arhiv_photo[1])
        if papka == 'okra':
           ss=2
           max=len(arhiv_photo[2])
        if papka == 'tatj':
           ss=3
           max=len(arhiv_photo[3])
        if papka == 'tatu':
           ss=4
           max=len(arhiv_photo[4])
        if papka == 'zubi':
           ss=5
           max=len(arhiv_photo[5])
        if int(nomers)>=max:
            nomers=str(0)		   
        if int(nomers) <0:
            nomers=str(max-1)				
        mnomer=str(int(nomers)-1)	
        pnomer=str(int(nomers)+1)		
        msg = bot.delete_message(c.message.chat.id, bib)
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='⬅️',callback_data='^'+papka+mnomer),types.InlineKeyboardButton(text='➡',callback_data='^'+papka+pnomer)) 
        keyboard.add(types.InlineKeyboardButton(text='Удалить фото',callback_data='delphoto'+papka+nomers))
        keyboard.add(types.InlineKeyboardButton(text='Добавить фото',callback_data='addphoto'+papka))		
        msg = bot.send_photo(c.message.chat.id, photo=open(papka+'/'+arhiv_photo[ss][int(nomers)], 'rb'),reply_markup=keyboard) 
############################# udalenie photo iz arhiva

    if 'delphoto' in c.data:
        papka=c.data[8:12]
        nomers=c.data[12:]
        if papka == 'make':
           del arhiv_photo[0][int(nomers)]
        if papka == 'nogt':
           del arhiv_photo[1][int(nomers)]
        if papka == 'okra':
           del arhiv_photo[2][int(nomers)]
        if papka == 'tatj':
           del arhiv_photo[3][int(nomers)]
        if papka == 'tatu':
           del arhiv_photo[4][int(nomers)]
        if papka == 'zubi':
           del arhiv_photo[5][int(nomers)]    
        msg = bot.delete_message(c.message.chat.id, bib)	
        output = open('arhiv_photo.pkl', 'wb')
        pickle.dump(arhiv_photo, output, 2)
        output.close()		
        msg = bot.send_message(c.message.chat.id, 'Фото удалено')
############################# dobavlenie_photo
    if 'addphoto' in c.data:
        papka=c.data[8:]
        if papka == 'make':
           admin_addphoto=0
        if papka == 'nogt':
           admin_addphoto=1
        if papka == 'okra':
           admin_addphoto=2
        if papka == 'tatj':
           admin_addphoto=3
        if papka == 'tatu':
           admin_addphoto=4
        if papka == 'zubi':
           admin_addphoto=5   
        msg = bot.delete_message(c.message.chat.id, bib)		
        msg = bot.send_message(c.message.chat.id, 'Отправте фото для добавления.') 
############################# dobavlenie kategorii procedur
    if c.data=='addkat':
        msg = bot.send_message(c.message.chat.id, 'Введите название категории(Не более 30 символов)')	
        admin_addkat=1	
############################# prosmotr kategorii adminom
    if 'adkat' in c.data:
        noms=int(c.data[5:])
        strins=''
        for i in range(0,len(procedures[noms])):
            strins+=procedures[noms][i]+'\n'     
        keyboard = types.InlineKeyboardMarkup(row_width=1)			
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addproc'+str(noms)) for name in ['Добавить процедуру']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delproc'+str(noms)) for name in ['Удалить процедуру']])        
        msg = bot.send_message(c.message.chat.id, 'Процедуры категории:\n'+strins,reply_markup=keyboard)
############################# dobavlenie proceduri v kategoriu
    if 'addproc' in c.data:		
        msg = bot.send_message(c.message.chat.id, 'Введите название процедуры(Не более 30 символов)') 
        noms=int(c.data[7:])
        admin_addproc	= noms	
############################# Sozdanie svazi
    if c.data=='addsvaz':
        new_svaz=svaz()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(kat_proc)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='adfksv'+str(i)) for name in [kat_proc[i]]])   
        msg = bot.send_message(c.message.chat.id, 'Укажите к какой категории будет предложение',reply_markup=keyboard)
    if 'adfksv' in c.data:
        noms=int(c.data[6:])
        new_svaz.from_kat=noms
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(procedures[noms])):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='adfpsv'+str(i)) for name in [procedures[noms][i]]]) 
        msg = bot.send_message(c.message.chat.id, 'Укажите к какой процедуре будет предложение',reply_markup=keyboard)		
    if 'adfpsv' in c.data:	
        noms=int(c.data[6:])
        new_svaz.from_proc=noms	
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(kat_proc)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='adtksv'+str(i)) for name in [kat_proc[i]]])   
        msg = bot.send_message(c.message.chat.id, 'Укажите из какой категории будет предложение',reply_markup=keyboard)
    if 'adtksv' in c.data:
        noms=int(c.data[6:])
        new_svaz.to_kat=noms
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(procedures[noms])):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='adtpsv'+str(i)) for name in [procedures[noms][i]]]) 
        msg = bot.send_message(c.message.chat.id, 'Укажите какая процедура будет предложена',reply_markup=keyboard)	
    if 'adtpsv' in c.data:	
        noms=int(c.data[6:])
        new_svaz.to_proc=noms	
        svazi.append(new_svaz)
        output = open('svazi.pkl', 'wb')
        pickle.dump(svazi, output, 2)
        output.close()
        msg = bot.send_message(c.message.chat.id, 'Связь добавлена \n'+kat_proc[svazi[-1].from_kat]+': '+procedures[svazi[-1].from_kat][svazi[-1].from_proc]+' -> '+kat_proc[svazi[-1].to_kat]+': '+procedures[svazi[-1].to_kat][svazi[-1].to_proc])
######################################### udalenie procedur
    if 'delproc' in c.data:		
        noms=int(c.data[7:])
        admin_addkat=noms
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(procedures[noms])):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delpts'+str(i)) for name in [procedures[noms][i]]]) 
        msg = bot.send_message(c.message.chat.id, 'Выберите какую процедуру удалить',reply_markup=keyboard) 
    if 'delpts' in c.data:		
        noms=int(c.data[6:])
        katis=admin_addkat
        admin_addkat=''
        for i in range(0,len(svazi)):
            if katis==svazi[i].from_kat and noms==svazi[i].from_proc:
                del svazi[i]
            if katis==svazi[i].to_kat and noms==svazi[i].to_proc:
                del svazi[i]                
        del procedures[katis][noms]               
        msg = bot.send_message(c.message.chat.id, 'Процедура и все связи с ней удалены')
    if c.data =='delkat': 
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(kat_proc)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='deljts'+str(i)) for name in [kat_proc[i]]]) 
        msg = bot.send_message(c.message.chat.id, 'Выберите какую категорию удалить',reply_markup=keyboard)   
    if 'deljts' in c.data:		
        noms=int(c.data[6:])
        for i in range(0,len(svazi)):
            if noms==svazi[i].from_kat:
                del svazi[i]
            if noms==svazi[i].to_kat:
                del svazi[i]                
        del procedures[noms]    
        del kat_proc[noms]		
        msg = bot.send_message(c.message.chat.id, 'Категория и все связи с ней удалены')
###########################  zakazivanie proceduri
    if 'zakaz' in c.data:
        noms=int(c.data[5:]) 
        bdpol[k].predloj[0]=noms		
        bdpol[k].zakaz=1	
        bdpol[k].zakazstr+=kat_proc[noms]+'\n'
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(procedures[noms])):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in [procedures[noms][i]]]) 
        msg = bot.send_message(c.message.chat.id, 'Выберите какую процедуру хотите заказать.',reply_markup=keyboard) 
        return()
    if bdpol[k].zakaz==1:
        bdpol[k].zakazstr+=c.data+'\n'
        for i in range(0,len(procedures[bdpol[k].predloj[0]])):
            if procedures[bdpol[k].predloj[0]][i] ==c.data:
                bdpol[k].predloj[1]=i
        bdpol[k].zakaz=0
        bdpol[k].zakaz1=1
        msg = bot.send_message(c.message.chat.id, 'Укажите дату на которую хотите заказать процедуру и комментарий') 
        return()
###########################  Udalenie svazei
    if 'delsvaz'==c.data:
        ss=''
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(svazi)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delsvz'+str(i)) for name in [str(i)]]) 
        for i in range(0,len(svazi)):
            ss+=str(i)+') '+kat_proc[svazi[i].from_kat]+': '+procedures[svazi[i].from_kat][svazi[i].from_proc]+' -> '+kat_proc[svazi[i].to_kat]+': '+procedures[svazi[i].to_kat][svazi[i].to_proc]+'\n'   
        msg = bot.send_message(c.message.chat.id, 'Какую связь удалить?\n'+ss,reply_markup=keyboard)    
    if 'delsvz' in c.data:
        noms=int(c.data[6:]) 
        del svazi[noms]
        keyboard = types.InlineKeyboardMarkup(row_width=1)			
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addsvaz') for name in ['Добавить связь']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delsvaz') for name in ['Удалить связь']]) 
        ss=''
        for i in range(0,len(svazi)):
            ss+=kat_proc[svazi[i].from_kat]+': '+procedures[svazi[i].from_kat][svazi[i].from_proc]+' -> '+kat_proc[svazi[i].to_kat]+': '+procedures[svazi[i].to_kat][svazi[i].to_proc]+'\n'         
        msg = bot.send_message(c.message.chat.id, 'Связь удалена.\nCвязи:\n'+ss,reply_markup=keyboard)        			
########################### Prosmotr arhiva procedur
    if 'arbla:' in c.data:
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        msg = bot.delete_message(c.message.chat.id, bib)		
        if zp==len(arhiv_procedur)-1:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arbla:'+str(zp-1)) for name in ['➡']]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otziv:'+str(len(arhiv_procedur)-2)) for name in ['Попросить оставить отзыв']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='debla:'+str(len(arhiv_procedur)-2)) for name in ['Удалить']])
        elif zp==0:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arbla:'+str(zp+1)) for name in ['⬅️']])  
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otziv:'+str(len(arhiv_procedur)-2)) for name in ['Попросить оставить отзыв']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='debla:'+str(len(arhiv_procedur)-2)) for name in ['Удалить']])	
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arbla:'+str(zp-1)) for name in ['➡']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arbla:'+str(zp+1)) for name in ['⬅️']]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otziv:'+str(len(arhiv_procedur)-2)) for name in ['Попросить оставить отзыв']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='debla:'+str(zp)) for name in ['Удалить']])				

        msg = bot.send_message(c.message.chat.id, arhiv_procedur[zp],reply_markup=keyboard) 	
######################### Udalenie zapisi o zakaze proceduri
    if 'debla:' in c.data:	
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        del arhiv_procedur[zp]
        msg = bot.delete_message(c.message.chat.id, bib)
        msg = bot.send_message(c.message.chat.id, 'Запись удалена')		
######################### Prosba otziva
    if 'otziv:' in c.data:	
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        for j in range(0,len(arhiv_procedur[zp])):
                if arhiv_procedur[zp][j]==' ':
                    phoneisk=arhiv_procedur[zp][:j]
                    break
        print(phoneisk)
        for i in range(0,len(bdpol)):
            if bdpol[i].phone==phoneisk:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Оставить отзыв']])	
                msg = bot.send_message(bdpol[i].id, 'Оставте отзыв, пожалуйста',reply_markup=keyboard) 				
        msg = bot.delete_message(c.message.chat.id, bib)
        msg = bot.send_message(c.message.chat.id, 'Запрос отправлен')	
######################### Ostavlenie otziva
    if c.data=='Оставить отзыв':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(arhiv_masterov)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otvmst'+str(i)) for name in [arhiv_masterov[i]]])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otvmst'+str(100)) for name in ['Я не помню мастера']])			
        msg = bot.send_message(c.message.chat.id, 'Выберите мастера который оказывал вам услуги.',reply_markup=keyboard)
    if 'otvmst' in c.data:
        noms=int(c.data[6:]) 
        if noms<90:		
            bdpol[k].otziv+=bdpol[k].name+'\nМастер: '+arhiv_masterov[noms]+'\n' 
        else:
            bdpol[k].otziv+=bdpol[k].name+'\n'		
        msg = bot.send_message(c.message.chat.id, 'Хорошо, теперь напишите текст отзыва.')



######################### dobavlenie mastera
    if c.data == 'addmast':
        admin_addmast=1
        msg = bot.send_message(c.message.chat.id, 'Укажите имя мастера(Не более 30 символов)') 
######################### udalenie mastera
    if c.data == 'delmast':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(arhiv_masterov)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delmst'+str(i)) for name in [arhiv_masterov[i]]])  
        msg = bot.send_message(c.message.chat.id, 'Какого мастера удалить?',reply_markup=keyboard)   	
    if 'delmst' in c.data:
        noms=int(c.data[6:]) 
        del arhiv_masterov[noms]      
        msg = bot.send_message(c.message.chat.id, 'Мастер удален') 
######################### Prosmotr arhiva otzivov polzovatelem
    if 'arotz:' in c.data:
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        msg = bot.delete_message(c.message.chat.id, bib)		
        if zp==len(arhiv_otzivov)-1:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arotz:'+str(zp-1)) for name in ['➡']]) 
        elif zp==0:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arotz:'+str(zp+1)) for name in ['⬅️']])  	
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arotz:'+str(zp-1)) for name in ['➡']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arotz:'+str(zp+1)) for name in ['⬅️']]) 
        msg = bot.send_message(c.message.chat.id, arhiv_otzivov[zp],reply_markup=keyboard) 			
#########################  Redaktirovanie otzivov
    if 'aaotz:' in c.data:
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        msg = bot.delete_message(c.message.chat.id, bib)		
        if zp==len(arhiv_otzivov)-1:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='aaotz:'+str(zp-1)) for name in ['➡']]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='deotz:'+str(len(arhiv_otzivov)-2)) for name in ['Удалить']])
        elif zp==0:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='aaotz:'+str(zp+1)) for name in ['⬅️']])  
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='deotz:'+str(len(arhiv_otzivov)-2)) for name in ['Удалить']])	
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='aaotz:'+str(zp-1)) for name in ['➡']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='aaotz:'+str(zp+1)) for name in ['⬅️']]) 
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='deotz:'+str(zp)) for name in ['Удалить']])				

        msg = bot.send_message(c.message.chat.id, arhiv_otzivov[zp],reply_markup=keyboard) 
###################### Udalenie otziva
    if 'deotz:' in c.data:	
        for i in range(0,len(c.data)):
            if c.data[i]==':':
                zp=int(c.data[i+1:])
                print(zp)
                break
        del arhiv_otzivov[zp]
        output = open('arotz.pkl', 'wb')
        pickle.dump(arhiv_otzivov, output, 2)
        output.close()
        msg = bot.delete_message(c.message.chat.id, bib)
        msg = bot.send_message(c.message.chat.id, 'Запись удалена')	
    if c.data=='bithpomen':
        msg = bot.send_message(c.message.chat.id, 'Введите новое поздравление.')
        bith_change=1		
    return()		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
def name(m):
    global bdpol, admin, admin_addkat, admin_addproc, svazi,arhiv_procedur, admin_addmast, admin_username,birthday_grac,bith_change,rassilka, arhiv_photo
    if m.chat.id<0:
        return()
    k=nomer(m.chat.id)
#########################   Vvod dati rojdenia
    bdpol[k].zakaz=0
    if bdpol[k].regpoz==1:
        if len(m.text)==5 and m.text[2]=='.' and m.text[0:2].isdigit() and m.text[3:5].isdigit():
            if int(m.text[0:2])<32 and int(m.text[3:5])<13:
                rr=1	
            else:
                rr=0			
        else:
            rr=0
        if rr==1:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['F.A.Q.','Заказать процедуру']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Отзывы о работе мастеров','Портфолио']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Хочу быть моделью']])
            msg = bot.send_message(m.chat.id, 'Спасибо за регистрацию, добро пожаловать в главное меню!',reply_markup=keyboard)
            bdpol[k].regpoz=0
            bdpol[k].bithday=m.text			
        else:
            msg = bot.send_message(m.chat.id, 'Данные введены неверно, попробуйте еще раз')	
##########################  Админ панель
    if bdpol[k].adminin==1:
        if m.text==admin_password:
            admin=m.chat.id
            admin_username='@'+m.from_user.username
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Архив заказов','Книга отзывов']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Процедуры','Связи процедур']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Шаблон поздравления ДР']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Рассылка','Портфолио']])
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['Архив моделей','Список мастеров']])
            msg = bot.send_message(m.chat.id, 'Добро пожаловать в админ панель.',reply_markup=keyboard)
            bdpol[k].adminin=0			
        else:
            msg = bot.send_message(m.chat.id, 'Данные введены неверно')	
            bdpol[k].adminin=0   
########################## rassilka
    if m.text=='Рассылка' and m.chat.id==admin:
            rassilka=1
            msg = bot.send_message(m.chat.id, 'Напишите сообщение для рассылки.')
            return()
    if rassilka==1 and m.chat.id==admin:
            rassilka=''
            for i in range(0,len(bdpol)):
                if i%20 ==0:
                    time.sleep(1)
                msg = bot.send_message(bdpol[i].id, m.text)
            msg = bot.send_message(m.chat.id, 'Сообщение отправлено всем пользователям')
##########################  Zapis na model       
    if m.text== 'Хочу быть моделью':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='model1') for name in ['Окрашивание']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='model2') for name in ['Прическа']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='model3') for name in ['Макияж']])
        msg = bot.send_message(m.chat.id, 'Моделью в какой категории хотите быть?',reply_markup=keyboard)        	
########################## Voprosi model okrashivanie
    if bdpol[k].model==1:
        bdpol[k].modelstr+='\nДлинна:'+m.text
        bdpol[k].model=2
        msg = bot.send_message(m.chat.id, 'Укажите исходный цвет.') 
        return()		
    if bdpol[k].model==2:
        bdpol[k].modelstr+='\nЦвет:'+m.text
        bdpol[k].model=3
        msg = bot.send_message(m.chat.id, 'Окрашены ли в настоящий момент волосы красителем?')  
        return()	
    if bdpol[k].model==3:
        bdpol[k].modelstr+='\nОкрашены ли в настоящий момент волосы красителем:'+m.text
        bdpol[k].model=4
        msg = bot.send_message(m.chat.id, 'Согласны ли вы на экспериментальное окрашивание, на усмотрение мастера?')
        return()	
    if bdpol[k].model==4:
        bdpol[k].modelstr+='\nСогласие на экстремальное окрашивание:'+m.text
        bdpol[k].model=5
        msg = bot.send_message(m.chat.id, 'По возможности отправьте мне фото волос, или напишите Нет, для пропуска этого вопроса.')
        return()	
    if bdpol[k].model==5 and m.text=='Нет':
        bdpol[k].modelstr+='\nФото:'+m.text
        bdpol[k].model=0
        arhiv_model.append(bdpol[k].modelstr)
        msg = bot.send_message(m.chat.id, 'Спасибо, заявка принята.')	
        bdpol[k].modelstr=''
        return()	
######################## voprosi model pricheska
    if bdpol[k].model==6: 
        bdpol[k].modelstr+='\nДлинна:'+m.text
        bdpol[k].model=7
        msg = bot.send_message(m.chat.id, 'Укажите пожалуйста оттенок волос ( брюнетка, блондинка, шатенка, рыжая).') 
        return()
    if bdpol[k].model==7: 
        bdpol[k].modelstr+='\nОттенок:'+m.text
        bdpol[k].model=0
        arhiv_model.append(bdpol[k].modelstr)
        msg = bot.send_message(m.chat.id, 'Спасибо, заявка принята.')	
        bdpol[k].modelstr=''
        print(arhiv_model)
        return()
####################### voprosi model makiaj
    if bdpol[k].model==8: 
        bdpol[k].modelstr+='\nВозраст:'+m.text
        bdpol[k].model=9
        msg = bot.send_message(m.chat.id, 'Присутствует ли на лице перманентный макияж?') 
        return()
    if bdpol[k].model==9: 
        bdpol[k].modelstr+='\nПерманентный макияж:'+m.text
        bdpol[k].model=10
        msg = bot.send_message(m.chat.id, 'Отправьте мне, пожалуйста, фото анфас.') 
        return()
######################## Prosmotr arhiva modelei
    if m.text=='Архив моделей' and m.chat.id==admin:
        if len(arhiv_model)==0:
            msg = bot.send_message(m.chat.id, 'В архиве нет записей')  
            return()			
        if len(arhiv_model)==1:	
            if arhiv_model[0][-1]=='$':
                print('ok eto photo')
                for i in range(1,len(arhiv_model[0])-1) :
                    zk=(i+1)*-1	
                    if 	arhiv_model[0][zk]==':':
                        photka=arhiv_model[0][zk+1:-1]
                        print(photka)					
                        msg = bot.send_photo(m.chat.id, photo=open('models/'+str(photka)+'.jpg', 'rb'),caption=arhiv_model[0])  
                        break
            else:
                msg = bot.send_message(m.chat.id, arhiv_model[0])             		
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='armod:'+str(len(arhiv_model)-2)) for name in ['➡']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='demod:'+str(len(arhiv_model)-1)) for name in ['Удалить']])		
        if arhiv_model[-1][-1]=='$':
            print('ok eto photo')
            for i in range(1,len(arhiv_model[-1])-1) :
                zk=(i+1)*-1	
                if 	arhiv_model[-1][zk]==':':
                    photka=arhiv_model[-1][zk+1:-1]
                    print(photka)					
                    msg = bot.send_photo(m.chat.id, photo=open('models/'+str(photka)+'.jpg', 'rb'),caption=arhiv_model[-1],reply_markup=keyboard)  
                    break
        else:
            msg = bot.send_message(m.chat.id, arhiv_model[-1],reply_markup=keyboard) 
######################### portfolio admina
    if m.text=='Портфолио' and m.chat.id==admin:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='^okra0') for name in ['Окрашивание']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='^nogt0') for name in ['Ногти']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='^make0') for name in ['Макияж']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='^tatu0') for name in ['Тату']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='^tatj0') for name in ['Татуаж']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='^zubi0') for name in ['Отбеливание зубов']])
        msg = bot.send_message(m.chat.id, 'Выберите портфолио',reply_markup=keyboard) 	
        return
#########################  Prosmotr portfolio
    if m.text=='Портфолио':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='$okra0') for name in ['Окрашивание']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='$nogt0') for name in ['Ногти']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='$make0') for name in ['Макияж']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='$tatu0') for name in ['Тату']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='$tatj0') for name in ['Татуаж']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='$zubi0') for name in ['Отбеливание зубов']])
        msg = bot.send_message(m.chat.id, 'Выберите портфолио',reply_markup=keyboard) 		
######################### Kategorii procedur admin
    if m.text=='Процедуры' and admin==m.chat.id:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(kat_proc)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='adkat'+str(i)) for name in [kat_proc[i]]])        
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addkat') for name in ['Добавить категорию']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delkat') for name in ['Удалить категорию']])          
        msg = bot.send_message(m.chat.id, 'Выберите категорию процедур',reply_markup=keyboard)       
######################### dobavlenie kategorii procedur
    if admin_addkat==1 and 	admin==m.chat.id:
        if len(m.text)>30:
            msg = bot.send_message(m.chat.id, 'Превышенно кол-во символов! Введите снова, но с меньшим кол-вом символов.')
            return()
        admin_addkat=0
        kat_proc.append(m.text)
        procedures.append([])
        output = open('kat.pkl', 'wb')
        pickle.dump(kat_proc, output, 2)
        output.close()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(kat_proc)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='adkat'+str(i)) for name in [kat_proc[i]]])        
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addkat') for name in ['Добавить категорию']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delkat') for name in ['Удалить категорию']])        
        msg = bot.send_message(m.chat.id, 'Категория добавлена.',reply_markup=keyboard) 		
######################### dobavlenie proceduri        
    if admin_addproc!='' and 	admin==m.chat.id:
        if len(m.text)>30:
            msg = bot.send_message(m.chat.id, 'Превышенно кол-во символов! Введите снова, но с меньшим кол-вом символов.')
            return()
        procedures[admin_addproc].append(m.text)
        output = open('procedures.pkl', 'wb')
        pickle.dump(procedures, output, 2)
        output.close()
        noms=admin_addproc
        admin_addproc=''
        strins=''
        for i in range(0,len(procedures[noms])):
            strins+=procedures[noms][i]+'\n'   
        keyboard = types.InlineKeyboardMarkup(row_width=1)			
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addproc'+str(noms)) for name in ['Добавить процедуру']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delproc'+str(noms)) for name in ['Удалить процедуру']])        
        msg = bot.send_message(m.chat.id, 'Процедуры категории:\n'+strins,reply_markup=keyboard)         
########################## Menu ukazania svezei procedur
    if m.text=='Связи процедур' and 	admin==m.chat.id:
        keyboard = types.InlineKeyboardMarkup(row_width=1)			
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addsvaz') for name in ['Добавить связь']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delsvaz') for name in ['Удалить связь']]) 
        ss=''
        for i in range(0,len(svazi)):
            ss+=kat_proc[svazi[i].from_kat]+': '+procedures[svazi[i].from_kat][svazi[i].from_proc]+' -> '+kat_proc[svazi[i].to_kat]+': '+procedures[svazi[i].to_kat][svazi[i].to_proc]+'\n'         
        msg = bot.send_message(m.chat.id, 'Тут вы можете установить предложение одной процедуры после другой \n Cвязи:\n'+ss,reply_markup=keyboard)   
######################### Zakaz proceduri
    if m.text=='Заказать процедуру':
        bdpol[k].zakazstr=bdpol[k].phone+' '+bdpol[k].name+'\n'
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(0,len(kat_proc)):
            keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='zakaz'+str(i)) for name in [kat_proc[i]]]) 
        msg = bot.send_message(m.chat.id, 'Выберите категорию процедуры',reply_markup=keyboard)        
    if bdpol[k].zakaz1==1:
        bdpol[k].zakaz1=0
        bdpol[k].zakazstr+=m.text
        msg = bot.send_message(m.chat.id,'Спасибо, вскоре с вами свяжется администратор.')
        for i in range(0,len(svazi)):
            if bdpol[k].predloj[0]==svazi[i].from_kat and 	bdpol[k].predloj[1]==svazi[i].from_proc:
                		        msg = bot.send_message(m.chat.id,'Так-же мы предлагаем взять вам '+kat_proc[svazi[i].to_kat]+' '+procedures[svazi[i].to_kat][svazi[i].to_proc])	
        msg = bot.send_message(admin,bdpol[k].zakazstr) 	
        arhiv_procedur.append(bdpol[k].zakazstr)
        output = open('arproc.pkl', 'wb')
        pickle.dump(arhiv_procedur, output, 2)
        output.close()
        bdpol[k].zakazstr='' 
######################### Prosmotr arhiva zakazov
    if m.text=='Архив заказов' and admin==m.chat.id:
        if len(arhiv_procedur)==0:
            msg = bot.send_message(m.chat.id, 'В архиве нет записей')  
            return()			
        if len(arhiv_procedur)==1:	
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otziv:'+str(len(arhiv_procedur)-1)) for name in ['Попросить оставить отзыв']])
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='debla:'+str(len(arhiv_procedur)-1)) for name in ['Удалить']])
                msg = bot.send_message(m.chat.id, arhiv_procedur[0],reply_markup=keyboard)  
                return()           		
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arbla:'+str(len(arhiv_procedur)-2)) for name in ['➡']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='otziv:'+str(len(arhiv_procedur)-1)) for name in ['Попросить оставить отзыв']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='debla:'+str(len(arhiv_procedur)-1)) for name in ['Удалить']])		
        msg = bot.send_message(m.chat.id, arhiv_procedur[-1],reply_markup=keyboard)         	
##########################  Redaktirovanie spiska masterov
    if m.text == 'Список мастеров':
        keyboard = types.InlineKeyboardMarkup(row_width=1)			
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='addmast') for name in ['Добавить мастера']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='delmast') for name in ['Удалить мастера']])         
        ss=''
        for i in range(0,len(arhiv_masterov)):
            ss+=arhiv_masterov[i]+'\n'         
        msg = bot.send_message(m.chat.id, 'Тут вы можете редактировать список мастеров\nМастера:\n'+ss,reply_markup=keyboard)
##########################  dobavlenie mastera
    if m.chat.id==admin and admin_addmast==1:
        if len(m.text)>30:
            msg = bot.send_message(m.chat.id, 'Превышенно кол-во символов! Введите снова, но с меньшим кол-вом символов.')
            return()
        arhiv_masterov.append(m.text)
        admin_addmast=0
        output = open('armas.pkl', 'wb')
        pickle.dump(arhiv_masterov, output, 2)
        output.close()		
        msg = bot.send_message(m.chat.id, 'Мастер добавлен')
########################## dobavlenie otziva
    if bdpol[k].otziv!='':
        bdpol[k].otziv+=m.text	
        arhiv_otzivov.append(bdpol[k].otziv)
        bdpol[k].otziv=''		
        output = open('arotz.pkl', 'wb')
        pickle.dump(arhiv_otzivov, output, 2)
        output.close()
        msg = bot.send_message(m.chat.id, 'Отзыв отправлен')
########################## Prosmotr arhiva otzivov polzovatelem
    if m.text=='Отзывы о работе мастеров':
        if len(arhiv_otzivov)==0:
            msg = bot.send_message(m.chat.id, 'В архиве нет записей')  
            return()			
        if len(arhiv_otzivov)==1:	
                msg = bot.send_message(m.chat.id, arhiv_otzivov[0])  
                return()           		
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='arotz:'+str(len(arhiv_otzivov)-2)) for name in ['➡']])		
        msg = bot.send_message(m.chat.id, arhiv_otzivov[-1],reply_markup=keyboard)		
########################### Redaktirovanie otzivov
    if m.text=='Книга отзывов' and m.chat.id==admin:
        if len(arhiv_otzivov)==0:
            msg = bot.send_message(m.chat.id, 'В архиве нет записей')  
            return()			
        if len(arhiv_otzivov)==1:	
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='deotz:'+str(len(arhiv_otzivov)-1)) for name in ['Удалить']])
                msg = bot.send_message(m.chat.id, arhiv_otzivov[0],reply_markup=keyboard)  
                return()           		
        keyboard = types.InlineKeyboardMarkup(row_width=1)

        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='aaotz:'+str(len(arhiv_otzivov)-2)) for name in ['➡']])
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='deotz:'+str(len(arhiv_otzivov)-1)) for name in ['Удалить']])		
        msg = bot.send_message(m.chat.id, arhiv_otzivov[-1],reply_markup=keyboard)    
#############################  F.A.Q 
    if  m.text=='F.A.Q.':
        msg =	bot.send_message(m.chat.id,'Введите ваш вопрос, я постараюсь на него ответить.')
        bdpol[k].vopros=1
        return()
    if bdpol[k].vopros==1:
        bdpol[k].vopros=0
        vopros=m.text
        if vopros[-1]=='.' or vopros[-1]=='?':
            vopros=vopros[:-1]
        vopros+=' '
        arrayslov=[]
        last=0
        ss=''
        for i in range(0,len(vopros)):
            if vopros[i]==' ':
                arrayslov.append(vopros[last:i].lower())
                last=i+1
        for i in range(0,len(procedures)):
            for j in range(0,len(procedures[i])):
                for z in range(0,len(arrayslov)):
                    if arrayslov[z] in procedures[i][j].lower():
                        ss+=kat_proc[i]+' '+procedures[i][j]+'\n'
					
        if ss!='':
            msg=bot.send_message(m.chat.id,'Вот что мы нашли по вашему запросу:\n'+ss+'Если это не то, что вы искали можете обратиться к нашему администратору: '+admin_username)  
            return()		
        msg=bot.send_message(m.chat.id,'Мы ничего не нашли по вашему вопросу, можете спросить у нашего администратора: '+admin_username)
############################  izmenenie pozdravlenia
    if m.text=='Шаблон поздравления ДР' and m.chat.id==admin:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data='bithpomen') for name in ['Да']])
        msg=bot.send_message(m.chat.id,'На данный момент поздравление таково: \n'+birthday_grac+'\nПоменять его?',reply_markup=keyboard) 
    if bith_change==1 and        m.chat.id==admin:
        birthday_grac=m.text
        msg=bot.send_message(m.chat.id,'Поздравление заменено на: \n'+birthday_grac)  
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)   
    output.close()      	
    		
		
		
		
		
		
		
		
		
		
####################################################### otsilaem kontakt	
@bot.message_handler(content_types=["contact"])
def check_chatid(message):
    print(message.contact.phone_number)
    global bdpol
    k=nomer(message.chat.id)
    bdpol[k].regpoz=1
    bdpol[k].phone=str(message.contact.phone_number)
    try:
        bdpol[k].name=message.from_user.first_name+' '+message.from_user.last_name 
    except Exception:
        bdpol[k].name=message.from_user.first_name
    msg = bot.send_message(message.chat.id, 'Напиши свою дату рождения. Обещаю, я никому не скажу. Это будет нашим маленьким секретом😉 (укажите свою дату рождения в формате ДД.ММ)')		   
    output = open('bdpol.pkl', 'wb')
    pickle.dump(bdpol, output, 2)
    output.close()

	
########################################### otpravka foto
@bot.message_handler(content_types=['photo'])
def photoget(message):
    global admin_addphoto
    k=nomer(message.chat.id)
    if bdpol[k].model==5:
        print(message)	
        nk=str(int(time.time()))
        fileid=(message.photo[2].file_id)
        bb=bot.get_file(fileid)
        bb=bb.file_path
        logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
        f = open("models/"+nk+'.jpg', "wb")
        f.write(logo)
        f.close()
        bdpol[k].modelstr+='\nФото:'+str(nk)+'$'        
        bdpol[k].model=0
        arhiv_model.append(bdpol[k].modelstr)
        msg = bot.send_message(message.chat.id, 'Спасибо, заявка принята.')	
        bdpol[k].modelstr=''
        output = open('armod.pkl', 'wb')
        pickle.dump(arhiv_model, output, 2)
        output.close()
    if bdpol[k].model==10:
        print(message)	
        nk=str(int(time.time()))
        fileid=(message.photo[2].file_id)
        bb=bot.get_file(fileid)
        bb=bb.file_path
        logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
        f = open("models/"+nk+'.jpg', "wb")
        f.write(logo)
        f.close()
        bdpol[k].modelstr+='\nФото:'+str(nk)+'$'        
        bdpol[k].model=0
        arhiv_model.append(bdpol[k].modelstr)
        msg = bot.send_message(message.chat.id, 'Спасибо, заявка принята.')	
        bdpol[k].modelstr=''
        print(arhiv_model)
        output = open('armod.pkl', 'wb')
        pickle.dump(arhiv_model, output, 2)
        output.close()
    if admin_addphoto!='' and message.chat.id==admin:
        nom=admin_addphoto
        admin_addphoto=''
		
        if nom==0:
            papka='make'
        if nom==1:
            papka='nogt'
        if nom==2:
            papka='okra'
        if nom==3:
            papka='tatj'
        if nom==4:
            papka='tatu'
        if nom==5:
            papka='zubi'
 
		
		
        nk=str(int(time.time()))
        fileid=(message.photo[2].file_id)
        bb=bot.get_file(fileid)
        bb=bb.file_path
        logo = urllib.request.urlopen("https://api.telegram.org/file/bot"+TOKEN+"/"+bb).read()
        f = open(papka+"/"+nk+'.jpg', "wb")
        f.write(logo)
        f.close() 
        arhiv_photo[nom].append(nk+'.jpg')	
        msg = bot.send_message(message.chat.id, 'Фото добавлено')	
        output = open('arhiv_photo.pkl', 'wb')
        pickle.dump(arhiv_photo, output, 2)
        output.close()			
############################################################### Hvost
	
def proverk():
    global bdpol
    now = datetime.datetime.now()
    if now.month<10:
        moth='0'+str(now.month)
    else:
        moth=str(now.month)
    if now.day<10:
        day='0'+str(now.day)
    else:
        day=str(now.day)
    for i in range(0,len(bdpol)):
        print(day,moth)
        print(bdpol[i].bithday)
        if bdpol[i].bithday==day+'.'+moth:
            msg=bot.send_message(bdpol[i].id, birthday_grac)		



schedule.every().day.at("11:40").do(proverk)
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
