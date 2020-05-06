#
# This file is used to train the LSTM model
#  
# Before running it, copy "company.txt", "relation.json" 
# "sentiment.json" and "label.json" to the current folder. 
#
# Usage:
# python ./rnn_lstm.py {PATH_TO_FIN_DATA} 
#
# Example:
# python ./rnn_lstm.py ../data/raw/fin_data
#


import collections
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
import os

from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

COMPANIES="./company.txt"
SENTI_PATH="./sentiment.json"
LABELS="./label.json"
RELATIONS = "./relation.json"

search_period = {
    "Q1": "ratios2018Q4",
    "Q2": "ratios2019Q1",
    "Q3": "ratios2019Q3",
    "Q4": "ratios2019Q4",
    "Q5": "ratios2020Q1",
}

# Combine the FIN ratios and sentiment data together
# Read the whole year in one time
def data_processing(fin_dir, period=None):
    # Load JSON files
    #print('period= {0}'.format(period))
    year_data = []
    for QQ in period:
        q_data = []
        fff = search_period[QQ] + ".json"
        abs_path = fin_dir + "/" + fff
        with open(abs_path) as f:
            q_data = json.load(f)
            year_data.append(q_data)

    with open(SENTI_PATH) as f:
        senti_data = json.load(f)
    
    with open(RELATIONS) as f:
        relation = json.load(f)

    with open(COMPANIES) as f:
        companies = [line.strip() for line in f]
    #print(companies) 
    
    final_data = []
    all_keys = []
    valid_list = []
    for i in range(0, len(period)):
        #print('the period is {0}'.format(period[i]))
        for key, val in year_data[i].items():
            find_str = key + "_" + period[i]
            combined = np.array(list(val.values()))
            
            if find_str in senti_data:
                combined = np.concatenate((combined, np.array(senti_data[find_str])))
            
            if find_str in relation:
                combined = np.concatenate((combined, np.array(relation[find_str])))

            # Save to the list
            final_data.append(combined)
            valid_list.append(find_str)
       

    ret = np.asarray(final_data)
    print(ret.shape)
    #padded = pad_sequences(final_data, padding='post')

    return ret, valid_list


def load_labels(fin_dir, period=None):
    year_data = []
    for QQ in period:
        q_data = []
        fff = search_period[QQ] + ".json"
        abs_path = fin_dir + "/" + fff
        with open(abs_path) as f:
            q_data = json.load(f)
            year_data.append(q_data)

    with open(COMPANIES) as f:
        companies = [line.strip() for line in f]
    
    #print(LABELS)
    with open(LABELS) as f:
        labels = json.load(f)
   
    sum = 0
    cnt = 0
    for val in labels.values():
        if val != "NA":
            sum = sum + val
            cnt = cnt + 1
    avg = sum * 1.0/cnt
    print('average value of the label is: {0}'.format(avg))

    final_data = []
    #valid_list = []
    for i in range(0, len(period)):
        for key, val in year_data[i].items():
            find_str = key + "_" + period[i]
            if labels[find_str] == None or labels[find_str] == "NA":
                # If there is no label found, use AVG directly.
                #print('No label found. {0}'.format(key))
                final_data.append(avg * 0.6)
            else:
                final_data.append(labels[find_str])
            #valid_list.append(find_str)

    """
    for ccc in companies:
        for i in range(0, len(period)):
            #print('the period is {0}'.format(period[i]))
            find_str = ccc + "_" + period[i]
            if labels[find_str] == None or labels[find_str] == "NA":
                # If there is no label, use "3.0" temporarily.
                # print('No label found. {0}'.format(ccc))
                final_data.append(avg)
                #final_data.append(np.nan)
            else:
                final_data.append(labels[find_str]/1.0)
    """

    return np.array(final_data)


def train_data(X, Y):
     # Split the data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    
    # XGBoost
    xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.4, learning_rate = 0.6, max_depth = 10, alpha = 10, n_estimators = 15)

    xg_reg.fit(X_train, Y_train)
    preds = xg_reg.predict(X_test)
    #print(preds)

    rmse = np.sqrt(mean_squared_error(Y_test, preds))
    print("RMSE: %f" % (rmse))

    score = xg_reg.score(X_test, Y_test)
    print(score)
    
    r2 = r2_score(Y_test, preds)
    print(r2)

    return xg_reg


def save_result(preds, keys):
    print(keys)
    data = {}
    for i in range(0, len(keys)):
        data[keys[i]] = str(preds[i])


    # save to json....
    with open("prediction.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



if __name__== "__main__":
    P = list(["Q1", "Q2", "Q3"])
    X, keys = data_processing(sys.argv[1], period= P)
    #np.info(X_train)

    Y = load_labels(sys.argv[1], period=P)
    #np.info(Y_train)
    
    xg_reg = train_data(X, Y)

    P = list(["Q4"])
    X, keys = data_processing(sys.argv[1], period= P)


    preds = xg_reg.predict(X)
    print("default prediction is:")
    print(preds)

    save_result(preds, keys)
   


