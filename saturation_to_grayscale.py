import time
import imageio
import colorsys
from multiprocessing import Pool, cpu_count

MODE = 0


def process(im, x):
    global MODE
    arr = []
    for y in range(len(im[x])):
        hsl = colorsys.rgb_to_hls(im[x][y][0] / 256.0, im[x][y][1] / 256.0, im[x][y][2] / 256.0)
        val = int(hsl[MODE] * 256)
        pix = [val, val, val]
        if len(im[x][y]) == 4:
            pix.append(255)
        arr.append(pix)
    return arr


done_count = 0
total_count = 0


def cb(state):
    global done_count, total_count
    done_count += 1
    print(done_count / total_count * 100)
    pass


if __name__ == '__main__':
    pool = Pool(processes=cpu_count())
    results = []

    im = imageio.imread('/Users/marstanjx/Desktop/test.png', 'png')
    total_count = len(im)

    start = time.time()
    for x in range(len(im)):
        results.append(pool.apply_async(func=process, args=(im, x,), callback=cb))

    count = 0
    for result in results:
        result.wait()
        arr = result.get()
        im[count] = arr
        count += 1
    end = time.time()


    pool.close()
    imageio.imsave('/Users/marstanjx/Desktop/export/0.png', im)

    duration = end - start
    print('Finished')
    print('%d seconds' % duration)
    speed = len(im) * len(im[0]) / duration
    print('%s pixel/second' % speed)
