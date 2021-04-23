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

    while True:
        c = input("\nDo you want to stop program:(Y/N) ")
        if c == 'Y' or c == 'y':
            stop_threads = True
            break

    x.join()

    print('thread killed')
