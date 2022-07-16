from ast import arg
import os
from tkinter import E
import pandas as pd
import argparse
import numpy as np

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

def get_data():
    URL  = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    try:
        df = pd.read_csv(URL, sep=";")
        return df
    except Exception as e:
        raise e

def evaluate(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual,pred))
    mae = mean_absolute_error(actual,pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2



def main(alpha, l1_ratio):
    df = get_data()

    train , test = train_test_split(df)
    
    train_x = train.drop(['quality'],axis=1)
    test_x = test.drop(['quality'],axis=1)

    train_y = train[['quality']]
    test_y = test[['quality']]
    #mlflow
    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        pred = lr.predict(test_x)

        rmse, mae, r2 = evaluate(test_y, pred)
        print(f"Elstic net params: alpha{alpha}, l1_ratio{l1_ratio}")
        print(f"Elstic net metrics: rmse{rmse}, mae{mae}, r2_score{r2}")
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)


    



if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--alpha","-a",type=float,required=False,default=0.5)
    args.add_argument("--l1_ratio","-l1",type=float,required=False,default=0.5)
    parsed_args = args.parse_args()
    try:
        main(alpha=parsed_args.alpha, l1_ratio=parsed_args.l1_ratio)
    except Exception as e:
        raise e
