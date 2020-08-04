# Risk-Analysis-on-Taiwanese-Companies

The English Premier is the top level of the English football league system. The goal of our work is to provide a system that has the function of 
* Team Performance Prediction
* Match Result Prediction
* Player Playstyle Clustering
* Player Influence Analysis.

## System Overview
The image below shows the overview of our system. 

<img src="readme_images/overview.png">
We used Google Cloud Platform (GCP) to store raw data and the preprocessed data and used Pyspark to process the csv data into RDD and do mapping and filtering for out feature extraction. For the prediction and classification models, we tried several tools: Keras, Scikit-learn, XGboost. We used Keras to build the LSTM model for performance prediction, and also the MLP model for match result classification. Scikit-learn was used to do several data preprocessing including one hot encoding, testing data splitting, and standard scaler. We also utilized the Random Forest classifier in Scikit-learn. 

## Prediction Models
The models of this work are prediction models(for team performance and match result) and analysis models(for playstyle clustering and influence analysis). We introduce our prediction models in this section.

<img src="readme_images/model.png">
The image above shows our match prediction model. We propose a method which combines our team performance algorithm(which is shown below) and the classification models we tested to solve the problem we encountered. The model is the combination of the LSTM model and Random Forest Classifier. 
<img src="readme_images/algo.png">

## Code Usage
For model comparing
```
python main.py compare [model] [method]
```
Available models: MLP, Forest, SVM, XGB, MLP <br>
Available methods: player, team

For prediction
```
python main.py predict
```
For clustering
```
python main.py cluster
```

## Contributors
This project is also contributed by Pei-Ling Tsai (pt2534@columbia.edu).
