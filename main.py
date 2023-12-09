from fastapi import FastAPI, HTTPException, Depends, Query
from datetime import datetime, timezone, timedelta
from typing import List
import web_scraping_price
import web_scrapping_additional
import concat_to_dataset
import backtests
from datetime import datetime

app = FastAPI()

def is_valid_time():
    obecny_czas_utc = datetime.now(timezone.utc)

    strefa_czasu_polska = timezone(timedelta(hours=1))
    obecny_czas_polska = obecny_czas_utc.astimezone(strefa_czasu_polska)

    if 9 <= obecny_czas_polska.hour < 10:
        return True
    else:
        return False

# Endpoint /update - updates data
@app.get('/update')
def update():
    web_scraping_price.Start_price_scraping()
    web_scrapping_additional.Start_additional_data_scraping()
    concat_to_dataset.Concat_to_dataset()

# Endpoint /predict
@app.get('/predict')
def predict():
    if is_valid_time():
        return 'yol'
    else:
        raise HTTPException(status_code=403, detail="Prognozy są dostępne tylko od 9:00 do 10:00.")

# Endpoint /backtest
@app.get('/backtest')
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