import sys
from io import BytesIO

import urllib.request
from bs4 import BeautifulSoup

import telegram
from flask import Flask, request, send_file
from time import sleep;
from fsm import TocMachine
#API_TOKEN = '488582332:AAE7swIh7w7ZM0sRUstZqubH5LKvHjz0Is0'
API_TOKEN='510481981:AAEZsN2FIDJLE7DCaM69BWDuzxguM5A-h_Q'
lastMessageId = 0;
bot = telegram.Bot(token=API_TOKEN);
machine = TocMachine(
    states=[
        'hasperson',
        'menu',
        'order',
        'phone',
        'news',
        'finish'
    ],
    transitions=[
        {
            'trigger': 'gomenu',
            'source':'hasperson',
            'dest': 'menu'
        },
        {
            'trigger': 'goorder',
            'source': 'hasperson',
            'dest': 'order'
        },
        {
            'trigger':'gonews',
            'source':'hasperson',
            'dest':'news'
        },
        {
            'trigger':'gophone',
            'source':'order',
            'dest':'phone'
        },    
        {
            'trigger': 'goback',
            'source': [
                'hasperson',
                'menu',
                'order',
                'phone',
                'news',
                'finish'
            ],
            'dest': 'hasperson'
        },
        {
            'trigger':'gofinish',
            'source':'phone',
            'dest':'finish',
        },
        {
            'trigger':'staymenu',
            'source':'menu',
            'dest':'menu'
        },
        {
            'trigger':'staynews',
            'source':'news',
            'dest':'news'
        }
    ],
    initial='hasperson',
    auto_transitions=False,
    show_conditions=True,
)

'''
def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

'''
def getText(Update):
    return Update["message"]["text"];

def getMessageId(Update):
    return Update["update_id"];

def getChatId(Update):
    return Update["message"]["chat"]["id"];

def getUserId(Update):
    return Update["message"]["from_user"]["id"];

def messageHandler(Update):
    global lastMessageId;
    text = getText(Update);
    msg_id = getMessageId(Update);
    user_id = getUserId(Update);
    lastMessageId = msg_id;
    if text =='/start':
        machine.trigger('goback');
    elif text =='order' and machine.state=='hasperson':
        #bot.sendMessage(user_id, '請問您要叫幾隻雞？');   
        machine.trigger('goorder');
    elif text =='news' and machine.state=='hasperson':
        #page=urllib.request.urlopen('http://home.so-net.net.tw/ywc580510/sale.html')
        #soup=BeautifulSoup(page.read(),"html.parser")
        #tmp=soup.find_all(width="168")
        #inf=tmp[1];
        #bot.sendMessage(user_id,inf.text)
        machine.trigger('gonews');
    elif text=='menu' and machine.state=='hasperson':
        #bot.sendPhoto(user_id,'http://home.so-net.net.tw/ywc580510/images/dmall.jpg');
        machine.trigger('gomenu');
    elif text!='/start' and machine.state=='menu':
        machine.trigger('staymenu');
    elif text!='/start' and machine.state=='news':
        machine.trigger('staynews');
    elif text!='/start' and machine.state=='order':
        machine.trigger('gophone');
    elif text!='/start' and machine.state=='phone':
        machine.trigger('gofinish');
    print("Message From User:");
    print(text);
    print("State:");
    print(machine.state);

    if machine.state=='hasperson':
        bot.sendMessage(user_id, '蛋蛋漢堡您好 點餐請輸入 order 觀看菜單請輸入 menu 欲知店家消息請輸入 news 重來請輸入 /start');
    elif machine.state=='menu':
        bot.sendPhoto(user_id,'http://home.so-net.net.tw/ywc580510/images/dmall.jpg');
    elif machine.state=='order':
        bot.sendMessage(user_id,'請輸入欲點的餐點：');
    elif machine.state=='news':
        page=urllib.request.urlopen('http://home.so-net.net.tw/ywc580510/sale.html')
        soup=BeautifulSoup(page.read(),"html.parser")
        tmp=soup.find_all(width="168")
        inf=tmp[1];
        bot.sendMessage(user_id,inf.text)
    elif machine.state=='phone':
        bot.sendMessage(user_id,'請輸入您的手機:'); 
    elif machine.state=='finish':
        bot.sendMessage(user_id,'完成訂購 歡迎下次光臨');
        machine.trigger('goback');        
        bot.sendMessage(user_id, '蛋蛋漢堡您好 點餐請輸入 order 觀看菜單請輸入 menu 欲知店家消息請輸入 news 重來請輸入 /start');
        print("State:");
        print(machine.state);
    return;

def main():
    global lastMessageId;
    Updates = bot.getUpdates();
    if(len(Updates) > 0):
        lastMessageId = Updates[-1]["update_id"];
    while(True):
        Updates = bot.getUpdates(offset=lastMessageId);
        Updates = [Update for Update in Updates if Update["update_id"] > lastMessageId]
        for Update in Updates:
            messageHandler(Update);
        sleep(0.5);
    
if __name__ == "__main__":
    main();
