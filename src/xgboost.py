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
    files_path = [os.path.join(fin_dir, x) for x in os.listdir(fin_dir)]
    #print(files_path)

    if period == None:
        period = duration
    
    # Load JSON files
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
    for ccc in companies:
        for i in range(0, len(period)):
            #print('the period is {0}'.format(period[i]))
            if ccc in year_data[i]:
                find_str = ccc + "_" + period[i]
                combined = np.array(list(year_data[i][ccc].values()))
                
                if find_str in senti_data:
                    combined = np.concatenate((combined, np.array(senti_data[find_str])))
                
                if find_str in relation:
                    combined = np.concatenate((combined, np.array(relation[find_str])))
        
            # Save to the list
            final_data.append(combined)
    
    ret = np.asarray(final_data)
    print(ret.shape)
    #padded = pad_sequences(final_data, padding='post')

    return ret


def load_labels(period=None):
    with open(COMPANIES) as f:
        companies = [line.strip() for line in f]
    
    #print(LABELS)
    with open(LABELS) as f:
        labels = json.load(f)
   

    final_data = []
    # TODO: Normalize the output ??
    for ccc in companies:
        for i in range(0, len(period)):
            #print('the period is {0}'.format(period[i]))
            find_str = ccc + "_" + period[i]
            if labels[find_str] == None or labels[find_str] == "NA":
                # If there is no label, use "3.0" temporarily.
                # print('No label found. {0}'.format(ccc))
                final_data.append(3.0/1.0)
                #final_data.append(np.nan)
            else:
                final_data.append(labels[find_str]/1.0)
       

    return np.array(final_data)


def train_data(x_train, y_train):
    pass


def test_data(x_test, y_test, model):
    pass


def predict_data(X):
    pass


if __name__== "__main__":
    P = list(["Q1", "Q2"])
    X = data_processing(sys.argv[1], period= P)
    #np.info(X_train)

    Y = load_labels(P)
    #np.info(Y_train)
    
    # Split the data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
    
    xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.4, learning_rate = 0.8, max_depth = 15, alpha = 10, n_estimators = 15)

    xg_reg.fit(X_train, Y_train)
    preds = xg_reg.predict(X_test)
    #print(preds)

    rmse = np.sqrt(mean_squared_error(Y_test, preds))
    print("RMSE: %f" % (rmse))

    score = xg_reg.score(X_test, Y_test)
    print(score)
    
    r2 = r2_score(Y_test, preds)
    print(r2)





