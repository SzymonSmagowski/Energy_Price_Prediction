from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timedelta
from typing import List

app = FastAPI()

# Przykładowe dane - prognozy cen na godzinę
fake_predictions = {
    "2023-12-08 09:00:00": 50.0,
    "2023-12-08 10:00:00": 51.5,
    # ... inne prognozy ...
}

def is_valid_time():
    current_time = datetime.now().time()
    return datetime.strptime("09:00:00", "%H:%M:%S").time() <= current_time < datetime.strptime("10:00:00", "%H:%M:%S").time()

# Endpoint /predict
@app.get('/predict')
def predict():
    if is_valid_time():
        return fake_predictions
    else:
        raise HTTPException(status_code=403, detail="Prognozy są dostępne tylko od 9:00 do 10:00.")

# Endpoint /backtest
@app.post('/backtest')
def backtest(dates: List[str]):
    if not dates:
        raise HTTPException(status_code=400, detail="Brak podanych dat do przeprowadzenia testu wstecznego.")

    predictions = {}
    for date in dates:
        # Tutaj można dodać logikę przewidywania cen na konkretną datę
        predictions[date] = fake_predictions.get(date, None)

    return predictions