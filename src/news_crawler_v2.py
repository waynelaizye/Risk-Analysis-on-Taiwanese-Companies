# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:50:33 2020

@author: Wayne
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import urlparse
import json
import os
import csv
import sys
import re
import urllib3
import time

# In some website, the article is not in <p>, so will be empty. Check articles 
# dictionary to delete empty news
skip_list = ['電腦及周邊設備', '上游', '下游']
file_name = 'test.txt'
save_path = 'president_news'
is_list = False


search_period = {
        "Q1": "min%3A1%2F1%2F2019%2Ccd_max%3A3%2F31%2F2019&tbm=nws",
        "Q2": "min%3A4%2F1%2F2019%2Ccd_max%3A6%2F30%2F2019&tbm=nws",
        "Q3": "min%3A7%2F1%2F2019%2Ccd_max%3A9%2F30%2F2019&tbm=nws",
        "Q4": "min%3A10%2F1%2F2018%2Ccd_max%3A9%2F31%2F2018&tbm=nws"
}

def read_list():
    print('Reading', file_name)
    word_list = []
    with open(file_name, encoding = 'utf8') as f:
        ff = f.read().splitlines()
    for line in ff:
        word_list.append(line.split(',')) 
    print('Total', len(word_list), 'lines')
    return word_list

def read_json():
    print('Reading', file_name)
    with open(file_name, encoding = 'utf8') as f:
        data = json.load(f)
    return data

def search(key_word="null", period=""):
    articles = {}

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if key_word == "null" or key_word in skip_list:
        #print("The key word is empty or in the skip list")
        return None
    
    keyword = quote(key_word.encode('utf8'))
    print('duration = {0}'.format(search_period[period]))
   
    # Sample request in Google search 
    # https://www.google.com/search?q=%E5%8F%B0%E7%A9%8D%E9%9B%BB&client=safari&rls=en&biw=1780&bih=946&source=lnt&tbs=cdr%3A1%2Ccd_min%3A7%2F1%2F2019%2Ccd_max%3A9%2F30%2F2019&tbm=nws
    res = requests.get("https://www.google.com/search?q=" + keyword + "&client=safari&rls=en&biw=1780&bih=946&source=lnt&tbs=cdr%3A1%2Ccd_" + search_period[period], verify=False)
    
    if res.status_code != 200:
        return articles

    headline = []
    soup = BeautifulSoup(res.text, 'lxml')
    a = soup.find_all('a') 
    for i in a:
        k = i.get('href')
        #print(k)
        try:
            m = re.search("(?P<url>https?://[^\s]+)", k)
            n = m.group(0)
            rul = n.split('&')[0]
            domain = urlparse(rul)
            if(re.search('google.com', domain.netloc)) or (re.search('zh.wikipedia.org', domain.netloc)):
                continue
            else:
                headline.append(rul)
        except:
            continue

    #print('total number of the news: {0}'.format(len(headline)))

    # Only iterate 100 posts
    for h in headline[0:100]:
        try:

            resp = requests.get(h,  allow_redirects=False)
            soup = BeautifulSoup(resp.content, 'html.parser')
#            test = soup.findAll(text = re.compile(key_word))
#            
#            if len(test) == 0:
#                print('Keyword {0} not found in webpage {1}'.format(key_word, h))
#                continue
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            #renewIPadress()
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            #renewIPadress()
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            #renewIPadress()
            continue
#        except KeyboardInterrupt:
#            print("Someone closed the program")

        # Concatenate all news together
        soup1 = BeautifulSoup(resp.content, "html.parser")
        lines = soup1.findAll('p')
        cont = ''
        for l in lines:
            cont += l.text
        articles[h] = cont
#        print(cont)

    return articles

def save_data(articles, word, save_path):
    word = word.replace(" ", "_")
    word = word.replace("/", "")
    print('file name = {0}'.format(word))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file = os.path.join(os.getcwd(),save_path, word + ".json")

    # save to json....
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

if __name__== "__main__":
#    word_list = read_list()
    print("This is news crawler")
    print('file = {0}, path = {1}'.format(file_name, save_path))
    if is_list:
        word_list = read_list()
        for words in word_list:
            articles = []
            name = words[0]
            for word in words:
                articles += search(word)
            save_data(articles, name, save_path)
    else:
        word_dic = read_json()
        for name in word_dic:
            for p in search_period:
                articles = {}
                for word in word_dic[name]:
                    articles.update(search(word, p))
                save_data(articles, name+'_'+p, save_path)
                time.sleep(1)