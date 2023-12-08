from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def change_latest_filename(directory, new_name):
    try:
        # Pobierz listę plików w danym katalogu
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # Sortuj pliki według daty modyfikacji (od najnowszego do najstarszego)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

        # Sprawdź, czy lista plików nie jest pusta
        if files:
            # Wybierz najnowszy plik
            latest_file = files[0]

            # Zbuduj nową ścieżkę dla pliku z nową nazwą
            new_path = os.path.join(directory, new_name)

            # Zmiana nazwy pliku
            os.rename(os.path.join(directory, latest_file), new_path)

            print(f"Najnowszy plik został pomyślnie zmieniony na {new_name}")

        else:
            print("Brak plików w katalogu.")

    except Exception as e:
        print("Wystąpił błąd:", str(e))


webdriver_path = 'edge_driver\\msedgedriver.exe'
url = 'https://www.pse.pl/dane-systemowe/plany-pracy-kse/plan-koordynacyjny-5-letni/wielkosci-podstawowe'


download_path = os.getcwd()
csv_file_path = os.path.join(download_path, 'plik.csv')


edge_options = webdriver.EdgeOptions()
edge_options.add_experimental_option('prefs', {'download.default_directory': download_path})

driver = webdriver.Edge(options=edge_options)
driver.get(url)

time.sleep(10)

csv_link = driver.find_element(By.CSS_SELECTOR, 'a[title="CSV"]')

csv_link.click()
time.sleep(10)

change_latest_filename(download_path, 'dane_tge.csv')