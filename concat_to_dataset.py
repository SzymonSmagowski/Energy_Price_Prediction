# some functions I have used for preprocessing
# I will use data from this dataset only, as an external factors
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from time import *
import os
from datetime import datetime, timedelta

def Read_csvs():
    try:
        dane_tge = pd.read_csv('data\\dane_kse.csv', encoding='unicode_escape', sep=';')
        prices = pd.read_csv('data\\newest_prices.csv')
    except Exception as e:
        print("Wystąpił błąd podczas zczytywania plików csv: ", str(e))
    return dane_tge, prices


def Delete_files():
    sciezki = ['data\\dane_kse.csv', 'data\\newest_prices.csv']
    for plik in sciezki:
        if os.path.isfile(plik) :
            os.unlink(plik)
        else :
            print("Plik nie istnieje.")
    return 


def Date_Fix(df):
    try:
        df['Doba'] = pd.to_datetime(df['Doba'])
        # df['Doba'] = np.where(df['Godzina'] == 24, df['Doba'] + pd.Timedelta("1 day") ,df['Doba'])
        # df['Godzina']  = np.where(df['Godzina'] == 24, 0 , df['Godzina'])
        df['Godzina']  = df['Godzina'].astype(int) - 1
        df["Doba_2"] = df["Doba"].astype(str) + ' ' + df["Godzina"].astype(str) + ':00:00.000000 UTC'
        df["Doba_2"] = pd.to_datetime(df["Doba_2"])
    except Exception as e:
        print("Wystąpił błąd podczas zamiany dat w pliku z KSE: ", str(e))
    return df


def Fill_na(df):
    try:
        df['Nadwy¿ka mocy dostêpna dla OSP ponad wymagan¹ rezerwê moc (5) - (4)'].fillna(0.0, inplace=True)
        df['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'].fillna(0.0, inplace=True)
        df.fillna(df.fillna(method='bfill'),inplace=True)
    except Exception as e:
        print("Wystąpił błąd podczas uzupełniania nulli: ", str(e))
    return df


def Create_index(df):
    try:
        df.index = df['Doba_2']
        df.index = pd.to_datetime(df.index)
    except Exception as e:
        print("Wystąpił błąd podczas ustawiania indeksu: ", str(e))
    return df


def Preprocess_prices(df):
    try:
        df = df.set_index('date')
        df.index = pd.to_datetime(df.index)
    except Exception as e:
        print("Wystąpił błąd podczas ustawiania indeksu cen: ", str(e))
    return df


def Concat_and_preprocess(dane_tge, prices):
    try:
        df_concat = dane_tge.merge(prices, how='inner', left_index=True, right_index=True)
        df_concat.index.name = 'Time'
        df_concat.fillna(method='bfill',inplace=True)
        df_concat = df_concat.drop(['Doba', 'Godzina', 'Doba_2'], axis = 1)
        df_concat.drop(df_concat.iloc[:, [1,2,3,4,5,13,14]], inplace=True, axis=1)
        df_concat.index = pd.to_datetime(df_concat.index)
        df_concat["day_of_week"] = df_concat.index.dayofweek
        df_concat["month"] = df_concat.index.month
        df_concat["hour"] = df_concat.index.hour
        df_concat['Niedyspozycyjnosc'] = df_concat['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹ca z ograniczeñ sieciowych wystêpuj¹cych w sieci przesy³owej oraz sieci dystrybucyjnej w zakresie dostarczania energii elektrycznej'].astype(int) + df_concat['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'].astype(int)
        df_concat.drop(['Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹ca z ograniczeñ sieciowych wystêpuj¹cych w sieci przesy³owej oraz sieci dystrybucyjnej w zakresie dostarczania energii elektrycznej','Prognozowana wielkoæ niedyspozycyjnoci wynikaj¹cych z warunków eksploatacyjnych JW wiadcz¹cych us³ugi bilansuj¹ce w ramach RB'], inplace=True, axis=1)
        df_concat['zrodla_odnawialne'] = df_concat['Prognozowana sumaryczna generacja róde³ wiatrowych'].astype(int) + df_concat['Prognozowana sumaryczna generacja róde³ fotowoltaicznych'].astype(int)
        df_concat.drop(['Prognozowana sumaryczna generacja róde³ wiatrowych','Prognozowana sumaryczna generacja róde³ fotowoltaicznych'], inplace=True, axis=1)
        df_concat['generacjaJW'] = df_concat['Przewidywana generacja JW i magazynów energii wiadcz¹cych us³ugi bilansuj¹ce w ramach RB (3) - (9)'].astype(int) + df_concat['Prognozowana generacja JW i magazynów energii nie wiadcz¹cych us³ug bilansuj¹cych w ramach RB'].astype(int)
        df_concat.drop(['Przewidywana generacja JW i magazynów energii wiadcz¹cych us³ugi bilansuj¹ce w ramach RB (3) - (9)','Prognozowana generacja JW i magazynów energii nie wiadcz¹cych us³ug bilansuj¹cych w ramach RB'], inplace=True, axis=1)
        df_concat.rename({'Planowane saldo wymiany miêdzysystemowej':'saldo'}, inplace=True, axis=1)

        order = ['Prognozowane zapotrzebowanie sieci', 'generacjaJW', 'zrodla_odnawialne','Niedyspozycyjnosc','saldo', 'month', 'day_of_week','hour','da1_price']
        df_concat = df_concat[order]
        df_concat['hour'] += 1
    except Exception as e:
        print("Wystąpił błąd podczas łączenia i przetwarzania cen i danych z ostatniego dnia:  ", str(e))
    return df_concat


def Read_full_dataset():
    try:
        full = pd.read_csv('data\\ready_dataset.csv')
        full.index = full['Time']
        full.drop(['Time'], axis=1, inplace=True)
    except Exception as e:
        print("Wystąpił błąd podczas zczytywania całego datasetu: ", str(e))
    return full

def Concat_to_dataset():
    dane_kse, prices = Read_csvs()
    dane_kse = Date_Fix(dane_kse)
    dane_kse = Fill_na(dane_kse)
    dane_kse = Create_index(dane_kse)
    prices = Preprocess_prices(prices)
    df_concat = Concat_and_preprocess(dane_kse, prices)
    try:
        full_dataset = pd.concat([Read_full_dataset(), df_concat])
        full_dataset.to_csv('data\\ready_dataset.csv')
    except Exception as e:
        print("Wystąpił błąd podczas łączenia i zapisu pliku całego zbioru danych: ", str(e))
    Delete_files()
    return
