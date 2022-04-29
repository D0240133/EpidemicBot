# 台中疫調
# Telegram Bot token:5230424166:AAHXfUQdDUUuxGXtWUZZthsyBtkkz15M5UI
# chanel link : https://t.me/+ifJdsVTqXKE2NDhl
# chat id : -1001766552745
import requests
import redis
import collections
import configparser
import os
from bs4 import BeautifulSoup
from telegram.ext import Updater # 更新者
from telegram.ext import CommandHandler, CallbackQueryHandler # 註冊處理 一般用 回答用
from telegram.ext import MessageHandler, Filters # Filters過濾訊息
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # 互動式按鈕

# 載入參數
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(ROOT_DIR + '/config.ini')

# 載入Redis
redisCli = redis.Redis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['db'], decode_responses=True)
finalDate = redisCli.get('beetalk_final_date')

# # telegram token
tgToken = config['telegram']['tgToken']
chat_id = config['telegram']['chat_id']

# 發送 request 取得台中疫調資訊
response = requests.get(
    "https://www.taichung.gov.tw/1789570/Lpsimplelist")

# 使用套件解析html    
soup = BeautifulSoup(response.text, "html.parser")

# 讀取最新疫調資料
latestRecord = soup.find("span", class_="date")
date = latestRecord.getText("span")
href = latestRecord.find_parent("a").get("href")
title = latestRecord.find_parent("a").get("title")
link = "https://www.taichung.gov.tw" + href

## 確認是否需發送訊息並處理相關資訊
try:
    if date != finalDate:
        # 發送訊息
        message = title + "\n疫調詳細資訊 : " + link
        requests.get(
            "https://api.telegram.org/bot" + tgToken + "/sendMessage?chat_id=" + chat_id + "&text=" + message
        )
        
        # 更新redis key
        redisCli.set('beetalk_final_date', date)
    else:
        print("疫調尚未更新")

except Exception as ex:
    print(ex)

