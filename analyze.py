from pymongo import MongoClient
import plotly.graph_objects as go
from datetime import datetime

print("Start Program")

client = MongoClient('localhost', 27017)
db = client['stockprice']
price = db['price']


def showStockPriceData(id, convert, interval, start_time, end_time):
    result = price.find({'id': id, 'convert': convert, 'price_timestamp': {'$lt': end_time, '$gt': start_time}})

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
    while True:
        id = input("id: ")
        convert = input("convert: ")
        interval = int(input("interval(s): "))
        start_day = input("start day: ")
        end_day = input("end day: ")

        showStockPriceData(id, convert, interval, start_day + 'T00:00:00Z', end_day + 'T00:00:00Z')

        print("")
        print("")

    x.join()

    print('thread killed')
