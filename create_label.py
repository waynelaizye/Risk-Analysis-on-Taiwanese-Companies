# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:07:06 2020

@author: Wayne
"""

stock = []
with open('fin_data\\stocks2018Q4.json', 'r', encoding='utf-8') as f:
    stock.append(json.load(f))
with open('fin_data\\stocks2019Q1.json', 'r', encoding='utf-8') as f:
    stock.append(json.load(f))
with open('fin_data\\stocks2019Q2.json', 'r', encoding='utf-8') as f:
    stock.append(json.load(f))
with open('fin_data\\stocks2019Q3.json', 'r', encoding='utf-8') as f:
    stock.append(json.load(f))
with open('fin_data\\stocks2019Q4.json', 'r', encoding='utf-8') as f:
    stock.append(json.load(f))
