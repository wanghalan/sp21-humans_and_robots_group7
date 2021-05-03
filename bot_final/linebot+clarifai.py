# -*- coding: UTF-8 -*-

# Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from imgurpython import ImgurClient
import configparser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from auth import authenticate
from datetime import datetime

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import urllib.parse,urllib.error,urllib.request,requests,wikipedia,os,json,sys,praw,bs4 as bs,time

line_bot_api = LineBotApi('4TlkzUJv9oQ6hotyXYD+++2AzeAmbahx/7OD3AKtNB8rwWtqk1vMxjZEHGLUcMs4JNdNhC/IKXCrzL/iusYEdEvBcJh3zhgk1h/5BmJsgIxTUrzoIull+KsWCtCjEhEi9LwwWluk58e3phrwGmxJogdB04t89/1O/w1cDnyilFU=')  # LineBot's Channel access token
handler = WebhookHandler('a43e17af025b6a82996e9091137da0b4')  # LineBot's Channel secret
user_id_set = set()  # LineBot's Friend's user id
app = Flask(__name__)


##############################################################################
album = None
image_path = 'dd.jpg'

def upload_image(client):
    """
    Uploads and image to imgur
    """

    config = {
        'album': album,
        'name': 'Ukulele Chords',
        'title': 'black face',
        'description': 'Chord chart generated: {0}'.format(datetime.now())
    }

    print('Uploading image...')
    image = client.upload_from_path(image_path, config=config, anon=False)
    print("Done")
    

    return image
##############################################################################


def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
    idFile = open('idfile', 'a')
    idFile.write(userId + ';')
    idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."


@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']  # get X-Line-Signature header value
    body = request.get_data(as_text=True)  # get request body as text
    print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)  # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=(ImageMessage, StickerMessage, TextMessage))
def handle_message(event):
    if isinstance(event.message, TextMessage):
        Msg = event.message.text
        print('GotMsg:{}'.format(Msg))

    ###########################################################################
        #if (event.message.type == "text"):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="你說了: " + event.message.text))
        
    elif isinstance(event.message, StickerMessage):
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=1))
    
    elif isinstance(event.message, ImageMessage):
        #line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url='https://i.imgur.com/VqsUWNQ.jpg', preview_image_url='https://i.imgur.com/VqsUWNQ.jpg'))
        message_content = line_bot_api.get_message_content(event.message.id)
        with open(r'C:\Users\Nico\Desktop\大二下\IOT\Final Project\bot_final\dd.jpg','wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        try:
            client = authenticate()
            image = upload_image(client)
            
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="上傳成功,圖片網址：{0}".format(image['link'])) #result in here 
            )
            
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))

################################################################################

    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # Reply API example

    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

    try:
        line_bot_api.push_message(userId, TextSendMessage(text='Thank you!!, im processing your image'))
        #sticker_message = StickerSendMessage(package_id='106', sticker_id='1')
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='2'))
        time.sleep(2)
        line_bot_api.push_message(userId, TextSendMessage(text='emmmm...., give me a minute'))
    #######################################################################################  clarifai API
        results = ' '
        app = ClarifaiApp(api_key='fe71b193ff3f4e95bb996226ed2397a1')
        model = app.models.get('food-items-v1.0')
        image = ClImage(
            url= image['link'])
        result = model.predict([image])
    #######################################################################################


        for each in result['outputs'][0]['data']['concepts']:
            # print(each['name']+', ',end='')
            # results=results+each['name']+','
            print(each['name'], ' ', each['value'])
            #line_bot_api.push_message(userId, TextSendMessage(text=each['name']))
            # print(results+'\n')

        line_bot_api.push_message(userId, TextSendMessage(text='hope you enjoy :D'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='132'))

    except:
        print('not an image url!!!!')
        line_bot_api.push_message(userId, TextSendMessage(text='wait...you sent me an invalid url, or did u even send me an image url?!'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='7'))
        pass

if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text='LineBot is ready for you.'))  # Push API example
    except Exception as e:
        print(e)

    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

