#
# This file is used to retrieve posts from Google news.
# Usage:
#
#

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import urlparse
import json
import os
import csv
import sys

# In some website, the article is not in <p>, so will be empty. Check articles 
# dictionary to delete empty news

skip_list = ['電腦及周邊設備', '上游', '下游']

def search(key_word="null"):
    articles = {}

    print('Key_word: {0}'.format(key_word))
    if key_word == "null" or key_word in skip_list:
        print("The key word is empty or in the skip list")
        return articles
    
    keyword = quote(key_word.encode('utf8'))
    
    res = requests.get("https://news.google.com/search?q=" + keyword + "when%3A4d&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant") #when%3A幾d 爬幾天之內新聞
    if res.status_code != 200:
        return articles
    
    soup = BeautifulSoup(res.content, "html.parser")
    headline = soup.findAll("a", {"class": "DY5T1d"})
    
    for h in headline:
        try:
            res1 = requests.get('https://news.google.com' + h['href'][1:], timeout=30)
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
        except KeyboardInterrupt:
            print("Someone closed the program")
            
        # Concatenate all news together
        soup1 = BeautifulSoup(res1.content, "html.parser")
        lines = soup1.findAll('p')
        cont = ''
        for l in lines:
            cont += l.text
        articles[h.text] = cont


    return articles


def parse_csv(file_name = "None", dest_path = "./"):
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            #print(row)
            if len(row) == 0:
                break
            if len(row) > 1:
                msg0 = search(row[0])
                if msg0 != None:
                    save_data(msg0, row[0], dest_path)
                
                if sys.argv[1] != "Relationship.csv":
                    msg1 = search(row[1])
                    if msg1 != None:
                        save_data(msg1, row[1], dest_path)
           
                    msg2 = search(row[2])
                    if msg2 != None:
                        save_data(msg2, row[2], dest_path)

    return True


def save_data(articles, file_name, path):
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace("/", "")
    print('file name = {0}'.format(file_name))
    dataset = path + "news_" + file_name + ".json"

    # save to json....
    with open(dataset, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)


if __name__== "__main__":
    print("This is news crawler")
    print('file = {0}, path = {1}'.format(sys.argv[1], sys.argv[2]))
    data = parse_csv(sys.argv[1], sys.argv[2])



