from urllib.request import urlopen
import json
import time
import datetime

from email_mars import send_email


def log(msg):
    print("[" + datetime.datetime.now().strftime("%Y/%m/%d, %I:%M%p") + "] \t" + msg)


def update(current_rate):
    send_email('Currency Rate Updates', "USD to CNY: " + str(current_rate))
    log("Email Sent!")


while True:
    url = 'https://api.exchangeratesapi.io/latest?base=USD&symbols=CNY'
    text = urlopen(url).read().decode('UTF-8')
    data = json.loads(text)

    rate = data['rates']['CNY']
    log("USD to CNY: " + str(rate))
    if rate <= 6.9 or rate >= 7:
        update(rate)
    time.sleep(600)
