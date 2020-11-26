import time
from datetime import datetime
import math

MAX_YS = 180
FILE = "data/ys.txt"


def print_ys(full_time):
    now = time.time()
    curr_ys = 160 - (full_time - now) / 60 / 8
    print("当前体力\t%d" % curr_ys)
    for t in [20, 40, 60, 80, 120, 160]:
        if curr_ys < t:
            dt = datetime.fromtimestamp(time.time() + (t - curr_ys) * 8 * 60)
            if dt.date() == datetime.fromtimestamp(time.time()).date():
                # today
                print("%d体力\t今天%d:%d" % (t, dt.hour, dt.minute))
            else:
                print("%d体力\t明天%d:%d" % (t, dt.hour, dt.minute))
    print("\n")


if __name__ == '__main__':
    f = open(FILE, "r")
    full_time = int(f.read())
    print("\n")
    print_ys(full_time)

    while True:
        v = input('输入体力变动（+40, -20...), s保存，q退出\n')
        change = 0
        if v == 'q':
            exit(0)
        if v == 's':
            f = open(FILE, "w")
            f.write("%d" % full_time)
            f.close()
            print("保存成功")
        elif v.startswith('+'):
            change = int(v[1:])
        elif v.startswith('-'):
            change = -int(v[1:])
        if change > 0:
            print("体力增加%d" % change)
        elif change < 0:
            print("体力减少%d" % change)
        print('\n')
        full_time += -change * 8 * 60
        print_ys(full_time)
