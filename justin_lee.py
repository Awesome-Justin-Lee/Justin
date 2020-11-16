import telegram
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests 
import json
import pandas as pd
from bs4 import BeautifulSoup
import logging
import emoji
import schedule
import time
import threading

# JSON data read
with open ('./stock_data.json',encoding = 'UTF-8') as json_file:
    json_data = json.load(json_file)
    json_data_2 = json_data['stock']['dataValues']

# make table using stock_data.json file
info_table = []
for idx,info in enumerate(json_data_2):
    code = info['stock_number']
    code_name = info['stock_name']
    price = info['stock_price']
    info_table.append([])
    info_table[idx].append(idx)
    info_table[idx].append(code)
    info_table[idx].append(price)
    info_table[idx].append(code_name)
    
# Active Bot with the token
token = "1461066934:AAHQLhV3b7PJ-EJX-JNJdYv0tz2fZBnWmhs"
bot = telegram.Bot(token)

# updater 
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# Pre-requirement Data for send_stock_recommendation
url = "https://finance.naver.com/item/main.nhn?code=" 
ment1 = "<<  끝투's 오늘의 추천 종목  >>\n\n"
ment = ment1
image = 'test_image.jpg'

# user_list = ["1437875774","1452320827" ]
user_list = ["1437875774" ]

# help page
help_text1 = "<<  끝투 사용방법 안내 >>\n\n1.  /help : 도움말 페이지 \n\n"
help_text2 = "2.  /recommend : 오늘의 추천 주식 \n\n3.  /buy : 주식구매 명령어"
help_text3 = "\n                 ex) 3번 주식을 20개 매수하려면\n                 /buy 3 20 을 입력하세요 \n"
help_text = help_text1 + help_text2 + help_text3
greeting_text = "끝투에 오신 것을 환영합니다!!\n"

    
    
# # delete it
chat_id = '1437875774'
custom_keyboard = [['1개','2개','3개'],['4개','5개','6개'],['7개','8개','9개'],['입력 완료','구매 취소']]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
bot.send_message(chat_id=chat_id, text="Custom Keyboard Test",  reply_markup=reply_markup)
time.sleep(10)
reply_markup = telegram.ReplyKeyboardRemove()
bot.send_message(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
    
# # delete it 2
# chat_id = '1437875774'
# custom_keyboard = [['top-left', 'top-right'],  ['bottom-left', 'bottom-right']]
# # custom_keyboard = [['top-left', 'top-right'],  ['bottom-left', 'bottom-right']]
# reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
# bot.send_message(chat_id=chat_id, text="Custom Keyboard Test",  reply_markup=reply_markup)
# time.sleep(10)
# reply_markup = telegram.ReplyKeyboardRemove()
# bot.send_message(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)


    
# Getting Stock Information
def get_stock_price(code):
    result = requests.get(url+code)
    bs_obj = BeautifulSoup(result.content,"html.parser")
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"}) # 태그 span, 속성값 blind 찾기
    now_price = blind.text
    return now_price

# make stock name as same length with each other
def equalizer(a):
    gong = ""
    for i in range (9-a):
        gong = gong + "  "
    return gong    

# make 'ment' for sending telegram
def send_stock_recommendation(json_data_2,user_id):
    now = time.localtime()
    url = "https://finance.naver.com/item/main.nhn?code=" 
    ment1 = "<<  끝투's 오늘의 추천 종목  >>\n"
    ment2 =  "현재시각 : %04d/%02d/%02d %02d:%02d:%02d\n\n" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    ment = ment1 + ment2
    image = 'test_image.jpg'    
    for idx,info in enumerate(json_data_2):
        code = info['stock_number']
        code_name = info['stock_name']
        name_len_a = len(code_name)
        price = info['stock_price']
        price = str(price)
        price = price.rjust(8)
        url_with_code = url + code
        updated_url = "[" + code_name + "]" + "(" + url_with_code + ")"
        temp = str(idx+1) + '. ' + updated_url + equalizer(name_len_a) +'가격'+price + '    매수 클릭\n\n'   ####you can use get_stock_price(code) for the price
        ment = ment + temp
    # send message to users     
    bot.sendMessage(chat_id = user_id,text = ment, parse_mode = 'Markdown',disable_web_page_preview=True)

# Defalult Greeting to all members
for user_id in user_list:   
    bot.send_photo(chat_id  = user_id, photo = open(image, 'rb'))
    bot.sendMessage(chat_id = user_id, text  = greeting_text)
    bot.sendMessage(chat_id = user_id, text  = help_text)    

# help page    
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= help_text)
    print(update.effective_chat.id)

start_handler = CommandHandler('help', help)
dispatcher.add_handler(start_handler)

# send stock_recommendation
def recommend(update, context):
    send_stock_recommendation(json_data_2,update.effective_chat.id)

start_handler = CommandHandler('recommend', recommend)
dispatcher.add_handler(start_handler)

#for priodical report
def report():
    for user_id in user_list:
        send_stock_recommendation(json_data_2,user_id)

# start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# sub-function for 'buy' function. 
def find_matching_stock_number(user_choice):
    return info_table[int(user_choice)-1][1]

# sub-function for 'buy' function. 
def find_matching_stock_price(user_choice):
    return info_table[int(user_choice)-1][2]

# sub-function for 'buy' function. 
def find_matching_stock_name(user_choice):
    return info_table[int(user_choice)-1][3]

# buy operation
def buy(update, context):
    user_want = update.message.text
    buy_commend,user_choice,user_quantity = user_want.split()
    user_stock_name = find_matching_stock_name(user_choice)
    user_stock_number = find_matching_stock_number(user_choice)
    user_stock_price = find_matching_stock_price(user_choice)
    buy_text1 = "고객님이 선택하신 ["
    buy_text2 = "] 주식을 ["
    buy_text3 = "원]에 ["
    buy_text4 = "]개 매수 하였습니다."
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=buy_text1+user_stock_name+buy_text2+user_stock_price+buy_text3+user_quantity+buy_text4)
    user_response_data = {
      "response": {
        "dataValues": [
            {
            "stock_number": user_stock_number,
            "stock_quantity" : user_quantity
            }
        ]
      }
    }
    with open("user_response.json", "w", encoding = "UTF-8") as json_file:
        json.dump(user_response_data, json_file, indent=4, sort_keys=True)

start_handler = CommandHandler('buy', buy)
dispatcher.add_handler(start_handler)

# sell operation
def sell(update, context):
    sell_text = "보유하고 있는 주식을 모두 매도하였습니다."
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text= sell_text)


start_handler = CommandHandler('sell', sell)
dispatcher.add_handler(start_handler)

#=========================================================

# def buy_stock_buttons_1(update, context):
#     task_buttons = [
#         [
#             InlineKeyboardButton( '1번 주식 매수', callback_data=1 ), 
#             InlineKeyboardButton( '2번 주식 매수', callback_data=2 )
#         ],
#         [   InlineKeyboardButton( '3번 주식 매수', callback_data=3 ), 
#             InlineKeyboardButton( '4번 주식 매수', callback_data=4 )
#         ],
#         [   InlineKeyboardButton( '5번 주식 매수', callback_data=5 ), 
#             InlineKeyboardButton( '구매 안함', callback_data=6 )
#         ]
#     ]
#     reply_markup = InlineKeyboardMarkup( task_buttons )
#     context.bot.send_message(chat_id=update.message.chat_id, text='매수할 주식을 선택해주세요.', reply_markup=reply_markup)

    
# def cb_button(update, context):
#     query = update.callback_query
#     data = query.data   
#     context.bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.TYPING)
#     user_stock_name = find_matching_stock_name(data)
#     user_stock_number = find_matching_stock_number(data)
#     user_stock_price = find_matching_stock_price(data)
#     if data == '6':
#         context.bot.edit_message_text(text='매수하지 않습니다.', chat_id=query.message.chat_id, message_id=query.message.message_id)
#     else:
#         context.bot.edit_message_text(text='[{}]의 매수할 수량을 입력해주세요.'.format(user_stock_name), chat_id=query.message.chat_id, message_id=query.message.message_id)       
#         task_buttons2 = [
#             [
#                 InlineKeyboardButton( '1개', callback_data=1 ), 
#                 InlineKeyboardButton( '2개', callback_data=2 ),
#                 InlineKeyboardButton( '3개', callback_data=3 ), 
#                 InlineKeyboardButton( '4개', callback_data=4 ), 
#                 InlineKeyboardButton( '5개', callback_data=5 )
#             ],
#             [   
#                 InlineKeyboardButton( '6개', callback_data=6 ), 
#                 InlineKeyboardButton( '7개', callback_data=7 ),
#                 InlineKeyboardButton( '8개', callback_data=8 ), 
#                 InlineKeyboardButton( '9개', callback_data=9 ), 
#                 InlineKeyboardButton( '10개', callback_data=10 )
#             ],
#             [   
#                 InlineKeyboardButton( '20개', callback_data=11 ), 
#                 InlineKeyboardButton( '30개', callback_data=12),
#                 InlineKeyboardButton( '50개', callback_data=13), 
#                 InlineKeyboardButton( '100개', callback_data=14 ), 
#                 InlineKeyboardButton( '500개', callback_data=15 )
#             ],
#             [   InlineKeyboardButton( '입력 완료', callback_data=16 ), 
#                 InlineKeyboardButton( '구매 취소', callback_data=17 )
#             ]
#         ]      
#         reply_markup = InlineKeyboardMarkup( task_buttons2 )
#         context.bot.send_message(chat_id=update.message.chat_id, text='매수할 주식을 선택해주세요.', reply_markup=reply_markup)
#         time.sleep(20)
#         context.bot.send_message(chat_id=update.effective_chat.id, text='[{}] 매수를 완료하였습니다.'.format( user_stock_name ))


    
# task_buttons_handler = CommandHandler( 'buy2', buy_stock_buttons_1 )
# button_callback_handler = CallbackQueryHandler( cb_button )    
 
# dispatcher.add_handler( task_buttons_handler )
# dispatcher.add_handler( button_callback_handler )
    
#=========================================================

#for scheduler
schedule.every(300).seconds.do(report)
def priodical_stock_data_report(interval):
    while True:
        schedule.run_pending()
        time.sleep(10) 

#for multi-threading (periodic_sending, and continous watchdog for query)
t = threading.Thread(target = priodical_stock_data_report, args=(30,))
t.start()

#for query watchdog 
while True:
    updater.start_polling(timeout=3, clean=False)
    updater.idle()
    time.sleep(1)
    