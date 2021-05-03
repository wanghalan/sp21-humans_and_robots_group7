# -*- coding: UTF-8 -*-

# Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import urllib.parse,urllib.error,urllib.request,requests,wikipedia,os,json,sys,praw,bs4 as bs,time


#For Web Crawler
import requests
from bs4 import BeautifulSoup

line_bot_api = LineBotApi('lAmBKK8an+RguZfZ/rtUTa8x9SRiujmCZ8qoc1ibD2YMmbL/tYdhWhm1XIwwYWdOZhuVeDC8yiBWChVld7GYtlcasGwKouJvSGF8TxQbvZvqFtXbSqdJ1G9JZaO0th0HLKiC5Q2QthlcSJdRpSpaZwdB04t89/1O/w1cDnyilFU=')  # LineBot's Channel access token
handler = WebhookHandler('4f210872f59e4e4ae3b1ba12e148ed16')  # LineBot's Channel secret
user_id_set = set()  # LineBot's Friend's user id
app = Flask(__name__)


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    if Msg == 'Hello, world': return
    print('GotMsg:{}'.format(Msg))

    # line_bot_api.reply_message(event.reply_token,TextSendMessage(text="收到訊息!!"))   # Reply API example

    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

    try:
        line_bot_api.push_message(userId, TextSendMessage(text='Thanks, I will process it.'))
        #sticker_message = StickerSendMessage(package_id='106', sticker_id='1')
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='2'))
        time.sleep(2)
        line_bot_api.push_message(userId, TextSendMessage(text='Please wait ^^'))
    #######################################################################################  clarifai API
        results = ' '
        app = ClarifaiApp(api_key='fe71b193ff3f4e95bb996226ed2397a1')
        model = app.models.get('food-items-v1.0')
        image = ClImage(
            url= Msg)
        result = model.predict([image])
    #######################################################################################

        crawl = []
        for each in result['outputs'][0]['data']['concepts']:
            # print(each['name']+', ',end='')
            # results=results+each['name']+','
            print(each['name'], ' ', each['value'])
            #line_bot_api.push_message(userId, TextSendMessage(text=each['name']))
            # print(results+'\n')
            crawl.append(each['name'])
            try:
                results = results + each['name'] + ','
            except:
                pass
        line_bot_api.push_message(userId, TextSendMessage(text='i see '+results))
        print(results)

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
                    item = "150"
                else:
                    item = soup.find("div", {"class": "Z0LcW"}).text.split(' ')[0]
                
                print(foods_name)   
                print("熱量: " + item + " kcal")
                line_bot_api.push_message(userId, TextSendMessage(text = foods_name + " : " + item + "  kcal"))

        line_bot_api.push_message(userId, TextSendMessage(text='All calories are for every 100g, hope you enjoy :D'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='132'))

    except:
        print('not an image url!!!!')
        line_bot_api.push_message(userId, TextSendMessage(text='wait...you sent me an invalid url, or did u even send me an image url?!'))
        line_bot_api.push_message(userId, StickerSendMessage(package_id='1', sticker_id='7'))
        pass

    # Google 搜尋 URL
    google_url = "https://www.google.com.tw/search"\

    # 設定 User-Agent (UA) 來假裝是透過瀏覽器做請求
    user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}



if __name__ == "__main__":

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            ################################################################################### push welcome text


            #line_bot_api.push_message(userId, TextSendMessage(text='Hallo there!!!'))
            #sticker_message = StickerSendMessage(
            #    package_id='1', sticker_id='134'
            #)
            #line_bot_api.push_message(userId, sticker_message)
            #line_bot_api.push_message(userId, TextSendMessage(text='I could tell you what dish u can make from the ingredients you have :D'))
            #time.sleep(3)
            #line_bot_api.push_message(userId, TextSendMessage(text='Please upload your ingredients photo to this link https://postimages.org/ and send me the \'Direct link\' at the bottom of your picture (.png), then i\'ll help you'))
            #time.sleep(2)

            #line_bot_api.push_message(userId, TextSendMessage(text='i dont expect any photos other than food tho *tehee*'))
            #sticker_message = StickerSendMessage(
            #    package_id='1', sticker_id='10'
            #)
            line_bot_api.push_message(userId, sticker_message)



            ###################################################################################
    except Exception as e:
        print(e)

    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)

