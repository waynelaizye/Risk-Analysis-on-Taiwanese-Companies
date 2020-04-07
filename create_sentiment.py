# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 05:49:33 2020

@author: Wayne
"""

import json
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import os

forest = pickle.load(open('forest_all.sav', 'rb'))
with open('company.txt', 'r', encoding='utf-8') as f:
    company_list = f.read().splitlines()

sentiments = {}
for c in company_list:
    sentiments[c+'_Q1'] = [0,0]
    sentiments[c+'_Q2'] = [0,0]
    sentiments[c+'_Q3'] = [0,0]
    sentiments[c+'_Q4'] = [0,0]

model = SentenceTransformer('distiluse-base-multilingual-cased')

files = os.listdir('news_posts')

for n in files:
    with open('news_posts\\'+ n, 'r', encoding='utf-8') as f:
        a = json.load(f)
    if a == {}:
        continue
    emb = model.encode(list(a.values()))
    sent = forest.predict_proba(emb)
    sentiments[n[5:-5]][0] = np.average(sent, axis = 0)[1]*2-1


files = os.listdir('ptt_company')

for n in files:
    with open('ptt_company\\'+ n, 'r', encoding='utf-8') as f:
        a = json.load(f)
    if a == []:
        continue
    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    for post in a:
        try:
            content = model.encode([post['content']])
            comment = model.encode([c['text'] for c in post['comment']])
        except:
            content = model.encode([post['title']]) # use title if no content
        try: # comment could be empty
            if post['date'] > '2019/09/30':
                Q4.append(forest.predict_proba(content)[0][1]*2-1)
                Q4.append(np.average(forest.predict_proba(comment),axis=0)[1]*2-1)
            elif post['date'] > '2019/06/30':
                Q3.append(forest.predict_proba(content)[0][1]*2-1)
                Q3.append(np.average(forest.predict_proba(comment),axis=0)[1]*2-1)
            elif post['date'] > '2019/03/30':
                Q2.append(forest.predict_proba(content)[0][1]*2-1)
                Q2.append(np.average(forest.predict_proba(comment),axis=0)[1]*2-1)
            elif post['date'] >= '2019/01/01':
                Q1.append(forest.predict_proba(content)[0][1]*2-1)
                Q1.append(np.average(forest.predict_proba(comment),axis=0)[1]*2-1)
        except:
            pass
    if Q1:
        sentiments[n[4:-5]+'_Q1'][1] = np.average(Q1)
    if Q2:
        sentiments[n[4:-5]+'_Q2'][1] = np.average(Q2)
    if Q3:
        sentiments[n[4:-5]+'_Q3'][1] = np.average(Q3)
    if Q4:
        sentiments[n[4:-5]+'_Q4'][1] = np.average(Q4)
    
with open('sentiment.json', 'w', encoding='utf-8') as f:
    json.dump(sentiments, f, ensure_ascii=False, indent=4)


