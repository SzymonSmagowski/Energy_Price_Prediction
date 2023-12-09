# Energy_Price_Prediction
Application in python that predicts energy price.

To start the app: 'uvicorn main:app --reload' in terminal. Then check docs on 'local_address'/docs

## Files (notebooks):
1. short_EDA_SARIMA_model - checking seasonality and stationarity of time series. Having few ideas. Created badly designed and implemented SARIMA model, however did not want to continue working with that. Switched on LSTM because of requirement about additional data sources.
2. read_dataset_EDA_LSTM - created full dataset of additional data (https://www.pse.pl/dane-systemowe/plany-pracy-kse/plan-koordynacyjny-5-letni/wielkosci-podstawowe) till present day. First successful attempt of creating LSTM model having these data as parameters + 48 parameters symbolizing change in prices for -x hour.
3. pre_processing - normalizing data, reducing dimentionality.

## Files (.py):
1. main.py - center of the application. API anchor.
2. web_scraping_price and additional - uses selenium to open browser and download both used datasets to files. (above and prices here: https://tge.pl/energia-elektryczna-rdn)
3. concat_to_dataset - uses scrapped data and joins it with full dataset. It's like an actualisation to the dataset. Deletes files.
4. backtests - creates new model and backtests it for given dates. 
5. prediction - webscraps additional data, creates new model and predict tomorrow's prices of energy.
6. prices_scraping_history - helper to scrap many prices datasets in the same run.
7. unittests - basic instance of unit testing. Not finished becuase many functions here works on dataframes themselves and returns them.

## Directories:
1. data - full dataset plus backup / temp scrapped data files.
2. results - images of evaluation of backtests / predictions and models evaluations.
