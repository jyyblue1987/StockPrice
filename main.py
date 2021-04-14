import threading
import time
import urllib.request as request

print("Start Program")

API_KEY = "7776525aa8b50c2410340e381ee02182"
def fetch_data_thread(stop):
    print("fetch_data_thread start")

    while stop() is not True:
        print("fetch data")
        url = f"https://api.nomics.com/v1/currencies/ticker?key={API_KEY}&ids=BTC&interval=1d&convert=USD&per-page=100&page=1"
        bdata = request.urlopen(url).read()
        data = bdata.decode('ascii')
        print("Data", data)
        time.sleep(5)


    print("fetch_data_thread end")


if __name__ == "__main__":
    stop_threads = False
    x = threading.Thread(target=fetch_data_thread, args=(lambda: stop_threads,))
    x.start()

    stop_threads = True

    x.join()

    print('thread killed')
