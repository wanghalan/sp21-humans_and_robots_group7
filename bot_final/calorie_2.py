import random
import requests
from bs4 import BeautifulSoup

crawl = ['pizza','tomato','crust','dough','cheese','mozzarella','pepperoni','vegetable','meat','basil','pie','salami','pepper','onion','ham','frozen pizza','chicken','pastry']

total_calories = 0
for i in range(len(crawl)):
	# Google 搜尋 URL
	google_url = "https://www.google.com.tw/search"

	# 查詢參數
	foods = crawl[i] + " calories"
	my_params = {"q": foods}

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
	       
	    print("每份含量: 100 g")
	    print("熱量: " + str(item) + " kcal")
	    total_calories = total_calories + float(item)

print(total_calories)