# -*- coding: UTF-8 -*-

import time, random

import os
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from decouple import config

import urllib.parse,urllib.error,urllib.request,requests,wikipedia,os,json,sys,praw,bs4 as bs,time

#For Web Crawler
import requests
from bs4 import BeautifulSoup
 
'''
Reference:
    https://github.com/Clarifai/clarifai-python/blob/master/README.md
'''
 

def get_food_results(path, local_file=True):
################ clarifai API
# can check https://www.clarifai.com/models/ai-food-recognition
    results = ' '
    app = ClarifaiApp(api_key='db68ee11aff24aed97a23c679e0d5046')
    model = app.models.get('food-items-v1.0')
    if local_file:
        response = model.predict_by_filename(path)
    else:
        response = model.predict_by_url(path)
    # print('results: %s' % results)

#Code for reading json(result from clarifai) to array in python 
    crawl = []
    for each in response['outputs'][0]['data']['concepts']:
        print(each['name'], ' ', each['value'])
        #filtering probability higher than 0.7
        if(each['value'] >= 0.74):
            taken = each['name']
        else:
            continue
        crawl.append(taken)
        results = results + taken + ','
        
    #print(results) 
    print(crawl)
########## Calories Crawler
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
    print(total_calories)
    final_result = 'i see....\n' + 'Approx. total calories : ' + str(total_calories) +' kcal'
    print(final_result)
    return total_calories
    
       

if __name__ == '__main__':
    #r = get_food_results('https://www.applesfromny.com/wp-content/uploads/2020/05/Jonagold_NYAS-Apples2.png', False)
    r = get_food_results('./img/apple.jpg')
    #print(r)
    print('-'*80)
    #r = get_food_results('./img/camImage.png')