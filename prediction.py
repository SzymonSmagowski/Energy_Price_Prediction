import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from time import *
from datetime import datetime, timedelta
import web_scrapping_additional
import concat_to_dataset
import unicodedata
import backtests
from sklearn.model_selection import train_test_split
import tensorflow as tf


def Fix_dataset(df):
    df.index = df['Doba_2']
    df.index.name = 'Time'
    df.fillna(method='bfill',inplace=True)
    df = df.drop(['Doba', 'Godzina', 'Doba_2'], axis = 1)
    df.drop(df.iloc[:, [1,2,3,4,5,13,14]], inplace=True, axis=1)
    df.index = pd.to_datetime(df.index)
    df["day_of_week"] = df.index.dayofweek
    df["month"] = df.index.month
    df["hour"] = df.index.hour
    df['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'] = df['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'].apply(lambda x: unicodedata.normalize("NFKD", x))
    df['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'] = df['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'].apply(lambda x: x.replace(' ',''))
    df['Niedyspozycyjnosc'] = df['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹ca z ograniczeñ sieciowych wystêpuj¹cych w sieci przesy³owej oraz sieci dystrybucyjnej w zakresie dostarczania energii elektrycznej'].astype(float) + df['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'].astype(float)
    df.drop(['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹ca z ograniczeñ sieciowych wystêpuj¹cych w sieci przesy³owej oraz sieci dystrybucyjnej w zakresie dostarczania energii elektrycznej','Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'], inplace=True, axis=1)
    df['zrodla_odnawialne'] = df['Prognozowana sumaryczna generacja róde³ wiatrowych'].astype(int) + df['Prognozowana sumaryczna generacja róde³ fotowoltaicznych'].astype(int)
    df.drop(['Prognozowana sumaryczna generacja róde³ wiatrowych','Prognozowana sumaryczna generacja róde³ fotowoltaicznych'], inplace=True, axis=1)
    df['generacjaJW'] = df['Przewidywana generacja JW i magazynów energii wiadcz¹cych us³ugi bilansuj¹ce w ramach RB (3) - (9)'].astype(int) + df['Prognozowana generacja JW i magazynów energii nie wiadcz¹cych us³ug bilansuj¹cych w ramach RB'].astype(int)
    df.drop(['Przewidywana generacja JW i magazynów energii wiadcz¹cych us³ugi bilansuj¹ce w ramach RB (3) - (9)','Prognozowana generacja JW i magazynów energii nie wiadcz¹cych us³ug bilansuj¹cych w ramach RB'], inplace=True, axis=1)
    df.rename({'Planowane saldo wymiany miêdzysystemowej':'saldo'}, inplace=True, axis=1)
    order = ['Prognozowane zapotrzebowanie sieci', 'generacjaJW', 'zrodla_odnawialne','Niedyspozycyjnosc','saldo', 'month', 'day_of_week','hour']
    df = df[order]
    df['hour'] += 1
    return df


def Load_full_dataset():
    df = pd.read_csv('data\\ready_dataset.csv', index_col='Time')
    return df


def Start_prediction(name = 'nowe_dane_kse.csv'):
    try:
        web_scrapping_additional.Start_additional_data_scraping(name)
        df = pd.read_csv(f'data\\{name}', sep=';', encoding='unicode_escape')

        tmr_date = datetime.now() + timedelta(days=1)
        tmr_date = tmr_date.strftime('%Y-%m-%d')

        df = df[df['Doba'] == tmr_date]
        df = concat_to_dataset.Date_Fix(df)
        df = Fix_dataset(df)
        df_full = Load_full_dataset()
        df_concat = pd.concat([df_full, df])
        df_concat = backtests.Normalize(df_concat)

        df = df_concat.iloc[-24:]
        df_concat = df_concat.iloc[:-24]
        for i in range(48):
            df_concat[f"hour-{i+1}"] = df_concat["da1_price"].shift(periods=i+1)
            df_concat = df_concat.dropna()
        last_record = df_concat.iloc[-1]

        X_train, X_test, y_train, y_test = train_test_split(
            df_concat.drop(['da1_price'], axis = 1), df_concat['da1_price'], test_size=0.25, random_state=42)

        model = backtests.Train_model_and_fit(X_train, y_train)
        model_lstm_preds = tf.squeeze(model.predict(X_test))
        predictions = model_lstm_preds.numpy()
        y_test.index = np.arange(len(y_test.index))

        backtests.Test_set_evaluation_save(y_test, predictions, str(str(tmr_date) + "_prediction_test_evaluation"))

        df = backtests.Add_cols(df)
        df.iloc[0] = backtests.Shift_first(df.iloc[0], last_record)
        df = df.drop(['da1_price'], axis=1)

        results = []
        tmp = model.predict(df.iloc[0].to_frame().T)
        results.append(tmp[0][0])
        i=1
        for elem in range(len(df)-1):
            df.iloc[i] = backtests.Shift_the_rest(df.iloc[i], df.iloc[i-1], results)
            tmp = model.predict(df.iloc[i].to_frame().T)
            results.append(tmp[0][0])
            i+=1

        output = []
        for x in range(24):
            output.append([f"Godzina {x}:00 :", str(round(results[x], 2))])

        backtests.Test_set_evaluation_save([], results, str(str(tmr_date) + "_prediction"))
        sciezka = f'data\\{name}'
    except Exception as e:
        print("Wystpił błąd podczas predykcji na następny dzień.")
    if os.path.isfile(sciezka) :
        os.unlink(sciezka)
    else:
        print("Plik nie istnieje.")
    return output