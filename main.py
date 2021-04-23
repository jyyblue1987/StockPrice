import threading
import time
import urllib.request as request
from pymongo import MongoClient
import json

import plotly.graph_objects as go
from datetime import datetime

print("Start Program")

client = MongoClient('localhost', 27017)
db = client['stockprice']
price = db['price']

API_KEY = "7776525aa8b50c2410340e381ee02182"
STOCK_IDS = "BTC,ETH,XRP"
def fetch_data_thread(stop):
    print("fetch_data_thread start")

    while stop() is not True:
        print("fetch data")
        url = f"https://api.nomics.com/v1/currencies/ticker?key={API_KEY}&ids={STOCK_IDS}&interval=1d&convert=USD&per-page=100&page=1"
        bdata = request.urlopen(url).read()
        res = bdata.decode('ascii')
        list = json.loads(res)

        for data in list:
            data['convert'] = 'USD'

            # find price data
            old = price.find_one({"id": data['id'], "convert": data["convert"], "price_timestamp": data["price_timestamp"]})
            if old is None:
                price_id = price.insert_one(data)
                print("Price Data is inserted successfully. ID: ", price_id)

        time.sleep(20)

    print("fetch_data_thread end")

def showStockPriceData(id, convert, interval):
    result = price.find({'id': id, 'convert': convert})

    open_data = []
    high_data = []
    low_data = []
    close_data = []
    dates = []

    start = None
    tm = None
    sub = []
    for row in result:
        val = float(row['price'])
        tm = datetime.strptime(row['price_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        if start is None:
            start = tm
            sub = [val]
        else:
            gap = tm - start
            seconds = gap.total_seconds()

            sub.append(val)

            if seconds >= interval:
                # collect data
                open = sub[0]
                close = sub[len(sub) - 1]
                high = max(sub)
                low = min(sub)

                open_data.append(open)
                close_data.append(close)
                high_data.append(high)
                low_data.append(low)

                dates.append(tm)

                start = None
                sub = []

    fig = go.Figure(data=[go.Candlestick(x=dates,
                                         open=open_data, high=high_data,
                                         low=low_data, close=close_data)])

    fig.show()



if __name__ == "__main__":
    stop_threads = False
    x = threading.Thread(target=fetch_data_thread, args=(lambda: stop_threads,))
    x.start()


    #
    # open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
    # high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
    # low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
    # close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
    # dates = [datetime(year=2013, month=10, day=10),
    #          datetime(year=2013, month=11, day=10),
    #          datetime(year=2013, month=12, day=10),
    #          datetime(year=2014, month=1, day=10),
    #          datetime(year=2014, month=2, day=10)]
    #
    # fig = go.Figure(data=[go.Candlestick(x=dates,
    #                                      open=open_data, high=high_data,
    #                                      low=low_data, close=close_data)])
    #
    # fig.show()

    while True:
        c = input("Please input command ")
        if c == 'Y' or c == 'y':
            stop_threads = True
            break
        if c == 'A': # analyze
            showStockPriceData('BTC', 'USD', 3600)

    x.join()

    print('thread killed')
