# -*- coding: utf-8 -*-
import csv
import os
import threading
from operator import itemgetter

files = []
tickers_data = {}
zero_volatility = []


class Ticker(threading.Thread):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.min = None
        self.max = None
        self.name_of_ticker = None
        self.volatility = None

    def run(self):
        self.find_min_max()
        self.find_volatility()

    def find_min_max(self):
        with open(self.file_name, 'r', encoding='cp1251') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            first_values = next(reader)
            self.name_of_ticker = first_values[0]
            self.min = float(first_values[2])
            self.max = float(first_values[2])
            for line in reader:
                try:
                    price = line[2]
                    price = float(price)
                    if price > self.max:
                        self.max = price
                    if price < self.min:
                        self.min = price
                except ValueError as exc:
                    print(exc)

    def find_volatility(self):
        average_price = round(self.max + self.min, 1) / 2
        self.volatility = round(self.max - self.min, 1) / average_price * 100
        self.volatility = round(self.volatility, 1)


def find_list_of_files():
    if os.path.exists('./trades'):
        for dirpath, dirnames, filenames in os.walk('./trades'):
            for every_file in filenames:
                full_file_path = os.path.join(dirpath, every_file)
                files.append(full_file_path)
    else:
        print('папки не существует')


def output(output_zero_volatility):
    sorted_tickers_data = sorted(tickers_data.items(), key=itemgetter(1), reverse=True)
    output_zero_volatility = ', '.join(output_zero_volatility)
    print('Максимальная волатильность')
    print(f'{sorted_tickers_data[0][0]} - {sorted_tickers_data[0][1]} %')
    print(f'{sorted_tickers_data[1][0]} - {sorted_tickers_data[1][1]} %')
    print(f'{sorted_tickers_data[2][0]} - {sorted_tickers_data[2][1]} %')
    print('Минимальная волатильность')
    print(f'{sorted_tickers_data[-1][0]} - {sorted_tickers_data[-1][1]} %')
    print(f'{sorted_tickers_data[-2][0]} - {sorted_tickers_data[-2][1]} %')
    print(f'{sorted_tickers_data[-3][0]} - {sorted_tickers_data[-3][1]} %')
    print('Нулевая волатильность')
    print(output_zero_volatility)


find_list_of_files()
tickers = [Ticker(file) for file in files]

for ticker in tickers:
    ticker.start()

for ticker in tickers:
    ticker.join()
    if ticker.volatility != 0.0:
        tickers_data[ticker.name_of_ticker] = ticker.volatility
    else:
        zero_volatility.append(ticker.name_of_ticker)
output(zero_volatility)
