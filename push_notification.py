from pync import Notifier
import os
import time

FILE = "data/ys.txt"

last = 0

while True:
    f = open(FILE, "r")
    full_time = int(f.read())
    curr_ys = int(160 - (full_time - time.time()) / 60 / 8)
    if last != curr_ys and curr_ys in [20, 40, 60, 80, 120, 160]:
        print('1')
        Notifier.notify('现在原石：%d' % curr_ys, title='原神')
    last = curr_ys
    time.sleep(10)
    Notifier.remove(os.getpid())
    Notifier.list(os.getpid())
