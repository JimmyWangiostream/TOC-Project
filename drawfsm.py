import sys
from io import BytesIO 
import urllib.request
from bs4 import BeautifulSoup 
import telegram
from flask import Flask, request, send_file
from time import sleep;
from fsm import TocMachine

lastMessageId = 0;
app = Flask(__name__)
WEBHOOK_URL='https://7f9e5916.ngrok.io/hook'
#API_TOKEN='500112032:AAGmab4De6gtWFBvywp-gc474K7H1DnLFWA'
API_TOKEN='488582332:AAE7swIh7w7ZM0sRUstZqubH5LKvHjz0Is0'
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
                    'news' ,
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

if __name__ == "__main__":
    _set_webhook()
    app.run(port=5000)

