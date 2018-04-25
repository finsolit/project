#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import os
import urllib
from telebot import types
API_TOKEN = '550267011:AAHyJ20FhScFC4ckcCW9RDNEyhKbWon3L2s'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(*[types.InlineKeyboardButton(text=name,callback_data=name) for name in ['❓ Часто задаваемые вопросы', '👌 Примеры работ','📲 Контакты']])
	msg = bot.send_message(message.chat.id, '<b>Добро пожаловать в Новый потолок!</b> 😊'+'\n'+'\n'+'Тут вы сможете:'+'\n'+
'❓ознакомиться с часто задаваемыми вопросами,'+'\n'+
'👌 посмотреть примеры работ,'+'\n'+
'📞 выйти на связь с нами',parse_mode='HTML',
	reply_markup=keyboard)



if __name__ == '__main__':
		bot.polling(none_stop=True)