import requests as rq
from bs4 import BeautifulSoup
import time
import requests
response = requests.get('https://www.pse.pl/dane-systemowe/plany-pracy-kse/plan-koordynacyjny-5-letni/wielkosci-podstawowe')
time.sleep(5)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.title)
string = str(soup).encode('ascii', 'ignore').decode('ascii')
# tables = soup.find_all('table', class_='p4NczRAMBVaGl__style_4')

# tables = soup.find(id="p4NczRAMBVaGl____bookmark_1")
#time.sleep(5)
#string = str(tables).encode('ascii', 'ignore').decode('ascii')
# for i in tables:
#     print(i.text)
f = open("tmp.txt", "w")
f.write(string)
f.close()