from fastapi import FastAPI, HTTPException, Depends, Query
from datetime import datetime, timezone, timedelta
from typing import List
import web_scraping_price
import web_scrapping_additional
import concat_to_dataset
import backtests
import prediction
from datetime import datetime

description = """
Documentation of endpoints: 🚀

Slightly differennt outputs as in description, but I thought it would look better.
Results are saved in folder /results with format:
'date'_task.png


* **Update dataset** (/update) 
Updates dataset for current day. That means it has to be done on daily basis before /predict.
* **Predict tomorrow's prices** (/predict)
Use only between 9.00 and 10.00. Downloads additional data for the next day and returns hourly predictions.
* **Backtesting** (/?dates=2023-12-07&dates=2023-03-11) - example.
Creates a new models for backtesting specyfic list of dates. Uses only data before that moment. 
"""

app = FastAPI(
    title="Energy Price Prediction",
    description=description,
    summary="Plus webscraping, model evaluation, EDA, etc.",
    version="1.0.0",
    contact={
        "name": "Szymon Smagowski",
        "email": "smagowski.szymon@gmail.com",
    },
)

def Is_valid_time():
    obecny_czas_utc = datetime.now(timezone.utc)

    strefa_czasu_polska = timezone(timedelta(hours=1))
    obecny_czas_polska = obecny_czas_utc.astimezone(strefa_czasu_polska)

    if 9 <= obecny_czas_polska.hour < 10:
        return True
    else:
        return False

# Endpoint /update - updates data
@app.get('/update',
        responses={
        401: {
            "description": "Not 401. Instead should be 'Internal server error.' - Error somewhere while updating dataset."
        },
        200: {
            "description": "OK",
            "content": {
                "application/json": {
                    "data": {"Godzina 1:": "Predykcja cena 1", "Godzina 2:": "Predykcja cena 2"}
                }
            },
        },
    },
)
def update():
    web_scraping_price.Start_price_scraping()
    web_scrapping_additional.Start_additional_data_scraping()
    concat_to_dataset.Concat_to_dataset()

# Endpoint /predict
@app.get('/predict', 
    responses={
        403: {"description": "Prognozy są dostępne tylko od 9:00 do 10:00."},
        200: {
            "description": "OK",
            "content": {
                "application/json": {
                    "data": {"Godzina 1:": "Predykcja cena 1", "Godzina 2:": "Predykcja cena 2"}
                }
            },
        },
    },
)
def predict():
    if Is_valid_time():
        predictions = {}
        date = datetime.now() + timedelta(days=1)
        date = date.strftime('%Y-%m-%d')
        predictions[date] = prediction.Start_prediction()
        return predictions
    else:
        raise HTTPException(status_code=403, detail="Prognozy są dostępne tylko od 9:00 do 10:00.")

# Endpoint /backtest
@app.get('/backtest',
    responses={
        401: {"description": "Nieprawidłowy format daty."},
        402: {"description": "Zakres dat jest nieprawidłowy"},
        200: {
            "description": "OK",
            "content": {
                "application/json": {
                    "data": {"Godzina 1:": "Predykcja cena 1", "Godzina 2:": "Predykcja cena 2"}
                }
            },
        },
    },
)
def backtest(dates: List[str] = Query(...)):
    predictions = {}
    if not dates:
        raise HTTPException(status_code=400, detail="Brak podanych dat do przeprowadzenia testu wstecznego.")

    predictions = {}
    for date in dates:
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except:
            raise HTTPException(status_code=401, detail="Nieprawidłowy format daty.")
        
        if not (datetime(2022, 12, 1) <= date < date.today()):
            raise HTTPException(status_code=402, detail="Zakres dat jest nieprawidłowy")
        
        predictions[date] = backtests.Backtest(str(date)) # converted to string, bo fastapi ma downa i nie obsługuje typów typu numpy
    return predictions