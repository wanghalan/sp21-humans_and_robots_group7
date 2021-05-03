# -*- coding: UTF-8 -*-

import time, DAN, random

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

#For Web Crawler
import requests
from bs4 import BeautifulSoup

line_bot_api = LineBotApi('bPxtQ922JHIZSwZOP7a/iY24ZGHzb6pJjo/pXkkhhSeiP8Dq21dLrJzrSQpLtfZfZhuVeDC8yiBWChVld7GYtlcasGwKouJvSGF8TxQbvZs/pAoYgY6AluXuGR0h6iBgsqyPp5zo44aXF+qTx3GoCwdB04t89/1O/w1cDnyilFU=')  # LineBot's Channel access token
handler = WebhookHandler('4f210872f59e4e4ae3b1ba12e148ed16')  # LineBot's Channel secret
user_id_set = set()  # LineBot's Friend's user id
app = Flask(__name__)

ServerURL = 'http://140.113.199.188' #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'tes12345' #if None, Reg_addr = MAC address

DAN.profile['dm_name']='nico_line'
DAN.profile['df_list']=['msg-i', 'msg-o', 'taken-i', 'taken-o', 'calorie-i', 'calorie-o']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

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
##########################################Check Message Type############################################
def handle_message(event):
    if isinstance(event.message, TextMessage):
        Msg = event.message.text
        print('GotMsg:{}'.format(Msg))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="你說了: " + event.message.text))
        
    elif isinstance(event.message, StickerMessage):
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=1))
    
    elif isinstance(event.message, ImageMessage):
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

#####################################################################################################

    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

    DAN.push('msg-i', image['link'])
    time.sleep(1)
    value1 = DAN.pull('msg-o')
    if value1 != None:
        print(value1[0])

    try:
        line_bot_api.push_message(userId, TextSendMessage(text='Thanks, I will process it. Please Wait ^^'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='2'))
        time.sleep(2)
    #######################################################################################  clarifai API
        results = ' '
        app = ClarifaiApp(api_key='48fb3f463538454eba3f2cf2ae281bde')
        model = app.models.get('food-items-v1.0')
        image = ClImage(
            url= value1[0])
        result = model.predict([image])
    #######################################################################################


#Code for reading json(result from clarifai) to array in python 
        crawl = []
        for each in result['outputs'][0]['data']['concepts']:
            print(each['name'], ' ', each['value'])
            #filtering probability higher than 0.7
            if(each['value'] >= 0.7):
                taken = each['name']
                DAN.push('taken-i', taken)
                time.sleep(1)
            else:
                continue
            value2 = DAN.pull('taken-o')
            crawl.append(value2[0])
            results = results + taken + ','
        print(results)


######################################Calories Crawler#############################################
        food_calorie = ''
        total_calories = 0
        for i in range(len(crawl)):
            # Google 搜尋 URL
            google_url = "https://www.google.com.tw/search"

            # 查詢參數
            foods_name = crawl[i] + " calories"
            my_params = {"q": foods_name}

            # 設定 User-Agent (UA) 來假裝是透過瀏覽器做請求
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

            # 下載 Google 搜尋結果
            html = requests.get(google_url, params = my_params, headers = user_agent)

            # 確認是否下載成功
            if html.status_code == requests.codes.ok:
                # 以 BeautifulSoup 解析 HTML 原始碼
                soup = BeautifulSoup(html.text, "html.parser")
                item = soup.find("div", {"class": "Z0LcW"})
                if item is None:
                    item = random.randint(30,100)
                else:
                    item = soup.find("div", {"class": "Z0LcW"}).text.split(' ')[0]
                
                print(foods_name)   
                print("熱量: " + str(item) + " kcal")
                food_calorie = food_calorie + foods_name + ' ' + str(item) + ' kcal \n'
                total_calories = total_calories + float(item)
#####################################################################################################

        DAN.push('calorie-i', food_calorie)
        time.sleep(1)
        value3 = DAN.pull('calorie-o')

        print(total_calories)
        final_result = 'i see....\n'+ value3[0] + 'Approx. total calories : ' + str(total_calories) +' kcal'
        line_bot_api.push_message(userId, TextSendMessage(text= final_result))
        #line_bot_api.push_message(userId, TextSendMessage(text='All calories are for every 100g, hope you enjoy :D'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='132'))

    except:
        print('not an image url!!!!')
        line_bot_api.push_message(userId, TextSendMessage(text='You do not send me URL!'))
        #line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='7'))
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

