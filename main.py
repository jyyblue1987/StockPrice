import threading
import time
import urllib.request as request
from pymongo import MongoClient
import json

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

if __name__ == "__main__":
    stop_threads = False
    x = threading.Thread(target=fetch_data_thread, args=(lambda: stop_threads,))
    x.start()

    import plotly.graph_objects as go
    from datetime import datetime

    open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
    high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
    low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
    close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
    dates = [datetime(year=2013, month=10, day=10),
             datetime(year=2013, month=11, day=10),
             datetime(year=2013, month=12, day=10),
             datetime(year=2014, month=1, day=10),
             datetime(year=2014, month=2, day=10)]

    fig = go.Figure(data=[go.Candlestick(x=dates,
                                         open=open_data, high=high_data,
                                         low=low_data, close=close_data)])

    fig.show()

    while True:
        c = input("Do you want to stop Program? (Y/N) ")
        if c == 'Y' or c == 'y':
            stop_threads = True
            break

    x.join()

    print('thread killed')
