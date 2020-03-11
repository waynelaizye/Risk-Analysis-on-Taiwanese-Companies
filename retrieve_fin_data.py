#
# This file is used to retrieve financial data from balance sheets.
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

def parse_csv(file_name = "None", dest_path = "./"):
    fin_data = {}

    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        index = 0
        for row in readCSV:
            #print(row)
            if len(row) == 0:
                break
            if len(row) > 1:
                if index == 0:
                    index = index +1
                    continue
                ratios = []
                #print('the whole row: {0}'.format(row))
                print('asset value: {0}'.format(float(row[6])))
                ratios.append(float(row[7]))
                
                tmp = float(row[9])*1.0/float(row[11])
                print(tmp)
                print('long-term debts/ total invested capital: {0}'.format(tmp))
                ratios.append(tmp)
                
                if row[10] != "--" and row[20] != "--" and float(row[20]) != 0:
                    print('debt/equity: {0}'.format(float(row[10])*1.0/float(row[20])))
                    ratios.append(float(row[10])*1.0/float(row[20]))
                else:
                    ratios.append("NULL")
                fin_data[row[4]] = ratios
    
    print('final result: {0}'.format(fin_data))
    
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
    print("Retrieving numbers from financial statements")
    print('file = {0}, path = {1}'.format(sys.argv[1], sys.argv[2]))
    data = parse_csv(sys.argv[1], sys.argv[2])








