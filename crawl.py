# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:53:48 2020

@author: Wayne
"""

url = 'https://news.ltn.com.tw/search?keyword=%E5%8F%B0%E7%A9%8D%E9%9B%BB&conditions=and&start_time=2019-11-23&end_time=2020-02-21'

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import urlparse

articles = {}
keyword = quote('台積電'.encode('utf8'))
res = requests.get("https://news.google.com/search?q=" + keyword + "when%3A1d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant")


if res.status_code == 200:
    soup = BeautifulSoup(res.content, "html.parser")
    headline = soup.findAll("a", {"class": "DY5T1d"})
    
    for h in headline:
        res1 = requests.get('https://news.google.com' + h['href'][1:])
        soup1 = BeautifulSoup(res1.content, "html.parser")
        lines = soup1.findAll('p')
        cont = ''
        for l in lines:
            cont += l.text
        articles[h.text] = cont

#res = requests.get('https://technews.tw/2020/02/20/face-foreign-investment-pass-tsmc-5-nanometers-full-in-advance/')
#content = res.content
#soup = BeautifulSoup(content, "html.parser")
#
#items = soup.findAll('p')
#cont = ''
#for i in items:
#    cont += i.text