import datetime
import os
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
save_path = 'C:\\Users\\marstan\\Desktop\\export'
data_dbfs = []
data_rms = []


def cal(_read_path, _file_name, _save):
    global data_dbfs, data_rms
    sound = AudioSegment.from_file(os.path.join(_read_path, _file_name))
    if sound.dBFS < -18:
        process = sound + 4
        process.export(os.path.join(_save, _file_name))


def cb(state):
    global count, curr
    log('(' + str(round(curr / count * 100, 2)) + '%)')
    curr += 1


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
                results.append(pool.apply_async(func=cal, args=(r, file, save_path,), callback=cb))
    for result in results:
        result.wait()
