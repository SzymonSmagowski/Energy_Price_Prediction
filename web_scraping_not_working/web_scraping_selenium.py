# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import numpy as np
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Driver's path
DRIVER_PATH = 'chromedriver\\chrome.exe'


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")

# Create a Service object
service = Service(DRIVER_PATH)

# Create a WebDriver instance using the Service object and the Chrome options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Starting site
site = 'http://www.google.com'
# site = 'https://justjoin.it/?employmentType=permanent&tab=with-salary'
driver.get(site)
driver.close()
# sleep(10)

# Find div element to scroll through
# div = driver.find_element(By.XPATH, '//div[@class="css-ic7v2w"]')