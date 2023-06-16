import json
import requests
import datetime
import os

plik_zapisu = "historia.txt"
if not os.path.exists(plik_zapisu):
    historia_sprawdzania = {}
else:
    with open(plik_zapisu, "r") as f:
        historia_sprawdzania = json.load(f)

sprawdzana_data = input('Podaj datę ( format daty : YYYY-MM-DD): ')

if sprawdzana_data == "":
    data_teraz = datetime.datetime.today() + datetime.timedelta(days=1)
    sprawdzana_data = data_teraz.strftime('%Y-%m-%d')

    if sprawdzana_data in historia_sprawdzania:
        dane = historia_sprawdzania[sprawdzana_data]
        print('data jest')
    else:
        api = requests.get(
            f'https://api.open-meteo.com/v1/forecast?latitude=53.78&longitude=20.49&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={sprawdzana_data}&end_date={sprawdzana_data}')
        dane = api.json()["daily"]["rain_sum"]
        print(dane)
        historia_sprawdzania[sprawdzana_data] = dane

elif len(sprawdzana_data) != 10 or sprawdzana_data.count('-') != 2 or \
        (sprawdzana_data.count('-') == 2 and (sprawdzana_data[4] != '-' or sprawdzana_data[7] != '-')):
    print('Nie poprawny format daty!')
    exit()

elif datetime.datetime.strptime(sprawdzana_data, '%Y-%m-%d') > datetime.datetime.today() + datetime.timedelta(days=16):
    print('Za duży zakres daty. Maksymalnie 16 dni od dzisiejszej daty!')
    exit()

elif sprawdzana_data in historia_sprawdzania:
    dane = historia_sprawdzania[sprawdzana_data]
    print('data jest')

else:
    api = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude=53.78&longitude=20.49&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={sprawdzana_data}&end_date={sprawdzana_data}')
    dane = api.json()["daily"]["rain_sum"]
    print(dane)
    historia_sprawdzania[sprawdzana_data] = dane

with open(plik_zapisu, "w") as f:
    json.dump(historia_sprawdzania, f)

if dane[0] == '' or dane[0] < 0:
    print('Nie wiem.')
elif dane[0] > 0:
    print('Bedzie padac')
elif dane[0] == 0:
    print('Nie bedzie padac')
