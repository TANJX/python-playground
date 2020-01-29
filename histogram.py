import datetime
import os
import matplotlib.pyplot as plt
from pydub import AudioSegment
from multiprocessing import Process, Pool, TimeoutError


def log(msg):
    print('[' + current_time_str() + '] ' + str(msg))


def current_time_str():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


curr = 0
count = 0
path = 'C:\\Users\\marstan\\AppData\\Roaming\\Anki2\\User 1\\collection.media\\'
save_path = 'C:\\Users\\marstan\\AppData\\Roaming\\Anki2\\User 1\\collection.media\\'
threshold = -18
data_dbfs = []
data_rms = []


def cal(_file):
    global data_dbfs, data_rms
    sound = AudioSegment.from_file(_file)
    return [sound.dBFS, sound.rms]


def cb(state):
    global count, curr
    log('(' + str(round(curr / count * 100, 2)) + '%)')
    curr += 1


def draw(graph, title, x, y):
    # matplotlib histogram
    plt.hist(graph, color='blue', edgecolor='black',
             bins=int(180 / 3))

    # Add labels
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()


if __name__ == '__main__':
    for r, d, f in os.walk(path):
        for file in f:
            (filename, ext) = os.path.splitext(file)
            if 'googletts' in filename:
                count += 1

    pool = Pool(processes=30)
    results = []

    for r, d, f in os.walk(path):
        for file in f:
            (filename, ext) = os.path.splitext(file)
            if 'googletts' in filename:
                curr_path = os.path.join(r, file)
                results.append(pool.apply_async(func=cal, args=(curr_path,), callback=cb))
    for result in results:
        data = result.get()
        data_dbfs.append(data[0])
        data_rms.append(data[1])

    draw(data_dbfs, 'Histogram of dBFS', 'dBFS', 'Num of Files')
    draw(data_rms, 'Histogram of rms', 'rms', 'Num of Files')
