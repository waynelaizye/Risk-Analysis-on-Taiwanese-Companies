# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:13:20 2020

@author: Wayne
"""

import requests

def getStock(id):
    p1 = '2018'
    site = 'https://query1.finance.yahoo.com/v7/finance/download/'+str(id) + \
    .TW?period1=0&period2=1549258857&interval=1d&events=history&crumb=hP2rOschxO0"
    stock = Share(str(id)+'.TW')
    today = datetime.date.today() #todays date
    data = stock.get_historical('2016-01-28', str(today))
    return data

print(getStock(2353))


site = "https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=0&period2=1549258857&interval=1d&events=history&crumb=hP2rOschxO0"
response = requests.post(site)