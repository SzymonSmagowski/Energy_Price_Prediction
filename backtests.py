import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from time import *
import os
from datetime import datetime, timedelta
from tensorflow.keras import layers
import tensorflow as tf
from sklearn.model_selection import TimeSeriesSplit
import math
from sklearn.model_selection import train_test_split

def Train_model_and_fit(X_train, y_train):
    # learning rate drop
    cb_reducelr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        mode="min",
        factor=0.1,
        patience=5,
        verbose=1,
        min_lr=0.000001
    )

    # early stopping
    cb_earlystop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        mode="min",
        min_delta=0.001,
        patience=10,
        verbose=1,
    )

    inputs = layers.Input(shape=(56))
    x = layers.Lambda(lambda x: tf.expand_dims(x, axis=1))(inputs) # expand a dimension
    x = layers.BatchNormalization()(x)
    x = layers.LSTM(512, activation="relu", return_sequences=True)(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.25)(x)
    x = layers.BatchNormalization()(x)
    x = layers.LSTM(512)(x)
    x = layers.BatchNormalization()(x)
    output = layers.Dense(1, activation="linear")(x)
    model_lstm = tf.keras.Model(inputs=inputs, outputs=output, name="model_lstm")

    # compile
    model_lstm.compile(loss="mse",
                     optimizer=tf.keras.optimizers.Adam(),
                     metrics=[tf.keras.metrics.RootMeanSquaredError()])
    
    model_lstm.fit(X_train, y_train,
             epochs=100,
             batch_size=128,
             verbose=0,
             validation_split = 0.2,
             callbacks=[cb_reducelr,
                        cb_earlystop])
    
    return model_lstm


def Date_format(date):
    return pd.to_datetime(date)


def Read_full_dataset():
    df = pd.read_csv('data\\ready_dataset.csv')
    return df


def Index_fix(df):
    df.index = df['Time']
    df.drop(['Time'], axis=1, inplace=True)
    return df


def Normalize(df):
    for col in df.drop(['da1_price','hour','month','day_of_week'], axis = 1).columns:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df


def Get_dates(date):
    date = date + ' 00:00:00+00:00'
    end_date = pd.to_datetime(date) + timedelta(hours=23)
    date = pd.to_datetime(date) - timedelta(hours=1)
    end_date = str(end_date) + '+00:00'
    date = str(date) + '+00:00'
    return date, end_date

# does not work ???
def Shift_working_dataset(working_dataset):
    for i in range(48):
        working_dataset[f"hour-{i+1}"] = working_dataset["da1_price"].shift(periods=i+1)
    working_dataset = working_dataset.dropna()
    return working_dataset


def Shift_first(row, last_row):
    row['hour-1'] = last_row['da1_price']
    for i in range(47):
        row[f'hour-{i+2}'] = last_row[f'hour-{i+1}']
    return row


def Shift_the_rest(row, last_row, list):
    row['hour-1'] = list[-1]
    for i in range(47):
        row[f'hour-{i+2}'] = last_row[f'hour-{i+1}']
    return row


def Add_cols(df):
    for i in range(48):
        df[f'hour-{i+1}'] = np.nan
    return df


def Test_set_evaluation_save(y_test, predictions, name):
    name = str(name).replace(':','_')
    plt.figure(figsize=(50,7))
    plt.plot(y_test, label="actual")
    plt.plot(predictions, label="predictions")
    plt.title("Prediction Performance")
    plt.legend()
    plt.savefig(f"results\\{name}")


# date = '2023-12-07'
def Backtest(date_start):
    output = []
    date, end_date = Get_dates(date_start)

    df = Read_full_dataset()
    df = Index_fix(df)
    df = Normalize(df)

    working_dataset  = df[:date]
    test_day = df[date:end_date]

    for i in range(48):
        working_dataset[f"hour-{i+1}"] = working_dataset["da1_price"].shift(periods=i+1)
    working_dataset = working_dataset.dropna()
    last_record = working_dataset.iloc[-1]

    X_train, X_test, y_train, y_test = train_test_split(
        working_dataset.drop(['da1_price'], axis = 1), working_dataset['da1_price'], test_size=0.25, random_state=42)
    
    model = Train_model_and_fit(X_train, y_train)
    model_lstm_preds = tf.squeeze(model.predict(X_test))
    predictions = model_lstm_preds.numpy()
    y_test.index = np.arange(len(y_test.index))

    Test_set_evaluation_save(y_test, predictions, str(str(date_start) + "_test_evaluation"))

    test_day = Add_cols(test_day)

    test_day.iloc[0] = Shift_first(test_day.iloc[0], last_record)
    actual_values = test_day['da1_price']
    test_day.drop(['da1_price'], axis=1, inplace=True)

    results = []
    tmp = model.predict(test_day.iloc[0].to_frame().T)
    results.append(tmp[0][0])

    i=1
    for elem in range(len(test_day)-1):
        test_day.iloc[i] = Shift_the_rest(test_day.iloc[i], test_day.iloc[i-1], results)
        tmp = model.predict(test_day.iloc[i].to_frame().T)
        results.append(tmp[0][0])
        i+=1
    
    for x in range(24):
        output.append([f"Godzina {x} actual,predicted: ",str(round(actual_values[x], 2)), str(round(results[x], 2))])
    
    Test_set_evaluation_save(actual_values, results, str(str(date_start) + "_day_backtest"))

    return output
