import json
import requests
import datetime
import os

class WeatherForecast:

    def __init__(self, plik_zapisu="historia.txt"):
        self.plik_zapisu = plik_zapisu
        self.historia_sprawdzania = {}

    def wczytaj_plik(self):
        if not os.path.exists(self.plik_zapisu):
            self.historia_sprawdzania = {}
            return self.historia_sprawdzania
        else:
            with open(self.plik_zapisu, "r") as f:
                self.historia_sprawdzania = json.load(f)
            return self.historia_sprawdzania

    def zapisz_plik(self):
        with open(self.plik_zapisu, "w") as f:
            json.dump(self.historia_sprawdzania, f)
            return self.historia_sprawdzania

    def sprawdzanie_daty(self, sprawdzana_data):
        if sprawdzana_data == "":
            data_teraz = datetime.datetime.today() + datetime.timedelta(days=1)
            sprawdzana_data = data_teraz.strftime('%Y-%m-%d')

            if sprawdzana_data in self.historia_sprawdzania:
                dane = self.historia_sprawdzania[sprawdzana_data]
                # print('data jest')
                return dane
            else:
                api = requests.get(
                    f'https://api.open-meteo.com/v1/forecast?latitude=53.78&longitude=20.49&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={sprawdzana_data}&end_date={sprawdzana_data}')
                dane = api.json()["daily"]["rain_sum"]
                # print(dane)
                self.historia_sprawdzania[sprawdzana_data] = dane
                return dane

        elif len(sprawdzana_data) != 10 or sprawdzana_data.count('-') != 2 or \
                (sprawdzana_data.count('-') == 2 and (sprawdzana_data[4] != '-' or sprawdzana_data[7] != '-')):
            print('Nie poprawny format daty!')
            exit()

        elif datetime.datetime.strptime(sprawdzana_data, '%Y-%m-%d') > datetime.datetime.today() + datetime.timedelta(
                days=16):
            print('Za duży zakres daty. Maksymalnie 16 dni od dzisiejszej daty!')
            exit()

        elif sprawdzana_data in self.historia_sprawdzania:
            dane = self.historia_sprawdzania[sprawdzana_data]
            # print('data jest')
            return dane

        else:
            api = requests.get(
                f'https://api.open-meteo.com/v1/forecast?latitude=53.78&longitude=20.49&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={sprawdzana_data}&end_date={sprawdzana_data}')
            dane = api.json()["daily"]["rain_sum"]
            # print(dane)
            self.historia_sprawdzania[sprawdzana_data] = dane
            return dane

    def __setitem__(self, sprawdzana_data, dane ):
        self.historia_sprawdzania[sprawdzana_data] = dane

    def __getitem__(self, sprawdzana_data):
        return self.historia_sprawdzania[sprawdzana_data]

    def __iter__(self):
        for x in self.historia_sprawdzania:
            yield x

    def items(self):
        for k, v in self.historia_sprawdzania.items():
            yield k,v


def odpowiedz(dane):
    if dane[0] == '' or dane[0] < 0:
        print('Nie wiem.')
    elif dane[0] > 0:
        print('Bedzie padac')
    elif dane[0] == 0:
        print('Nie bedzie padac')


obiekt = WeatherForecast()
obiekt.wczytaj_plik()
wejscie = input('Podaj datę ( format daty : YYYY-MM-DD): ')
if wejscie == "":
    data_teraz = datetime.datetime.today() + datetime.timedelta(days=1)
    wejscie = data_teraz.strftime('%Y-%m-%d')
else:
    wejscie = wejscie
obiekt[wejscie] = obiekt.sprawdzanie_daty(wejscie)
obiekt.zapisz_plik()
print(f'\nPpogoda dla podanej daty : {obiekt[wejscie]}\n')

print('Iterator dat dla, kótych znana jest pogoda:\n')
for data in obiekt:
    print(data)
print('\nGenerator tupli:\n')
for linia, idx in enumerate(obiekt.items()):
    print(linia + 1, idx)

odpowiedz(obiekt.sprawdzanie_daty(wejscie))

