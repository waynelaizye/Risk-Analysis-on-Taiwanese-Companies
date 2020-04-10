import collections
import matplotlib.pyplot as plt
import numpy as np
import keras
import json
import sys

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Embedding
from keras.layers import LSTM
#from keras.layers import Dense, Activation, Flatten

COMPANIES="./company.txt"

# Combine the FIN ratios and sentiment data together
def load_train_data(fin_path, senti_path, period):
    with open(fin_path) as f:
        fin_data = json.load(f)
    
    with open(senti_path) as f:
        senti_data = json.load(f)
  
    final_data = []
    for key, val in fin_data.items():
        combined = np.array(list(val.values()))
        find_str = key + "_" + period
        duration = []
        #print('keyword in sentiment: {0}, {1}'.format(key, find_str))
       
        if find_str in senti_data:
            combined = np.concatenate((combined, np.array(senti_data[find_str])))
        else:
            combined = np.concatenate((np.array(val), np.array([0.0, 0.0])))
        
        duration.append(combined)
        #print('keyword= {0}, data= {1}'.format(key, combined))
        final_data.append(np.array(duration))


    #print(final_data)
    return list(fin_data.keys()), np.array(final_data)

def load_labels(companies, path, period):
    with open(path) as f:
        labels = json.load(f)
   
    # TODO: Normalize the output
    output = []
    for ccc in companies:
        find_str = ccc + "_" + period
        if labels[find_str] == None or labels[find_str] == "NA":
            # If there is no label, use "3.0" temporarily.
            output.append(3.0/10.0)
        else:
            output.append(labels[find_str]/10.0)
   

    return np.array(output)


def train_data(x_train, y_train):
    max_features = len(x_train) * len(x_train[0])

    model = Sequential()
    
    # Add an embedding layer
    # model.add(Embedding(max_features, output_dim=128))
   
    print('X (row, col) = ({0}, {1})'.format(len(x_train), len(x_train[0])))
    print('Y (row, col) = {0}'.format(y_train.shape))
    # Add a LSTM layer with 128 internal units.
    model.add(LSTM(16, return_sequences=True, activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=10)


    return model

def test_data(x_test, y_test, model):
    score = model.evaluate(x_test, y_test, batch_size=16)
    print('the final score is: {0}'.format(score))


    return score
    

def output_scores():
    model = tf.keras.Sequential()
    model.add(layers.Embedding(input_dim=1000, output_dim=64))

    # The output of GRU will be a 3D tensor of shape (batch_size, timesteps, 256)
    model.add(layers.GRU(256, return_sequences=True))

    # The output of SimpleRNN will be a 2D tensor of shape (batch_size, 128)
    model.add(layers.SimpleRNN(128))

    model.add(layers.Dense(10))

    model.summary()


if __name__== "__main__":
    #load_train_data()
    keys, X_train = load_train_data(sys.argv[1], "./sentiment.json", "Q1")

    Y_train = load_labels(keys, "./label.json", "Q1")

    model = train_data(X_train, Y_train)

    keys, X_test = load_train_data(sys.argv[2], "./sentiment.json", "Q2")
    Y_test = load_labels(keys, "./label.json", "Q2")
    test_data(X_test, Y_test, model)
    #output_scores()

