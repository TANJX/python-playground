# from image_match.goldberg import ImageSignature
#
# gis = ImageSignature()
# a = gis.generate_signature('')
# b = gis.generate_signature('')
# gis.normalized_distance(a, b)
#

import os
import datetime
import random


def log(msg):
    print('[' + current_time_str() + '] ' + str(msg))


def current_time_str():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


path = 'C:\\Users\\marstan\\OneDrive\\Pictures\\Anime\\Anmi'

files = []
paths = []

img_exts = ['.jpg', '.jpeg', 'png']
signature_dict = {}

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        (filename, ext) = os.path.splitext(file)
        if ext in img_exts:
            full_name = os.path.join(r, file)
            paths.append(full_name.replace(path, ''))
            files.append(file)
            signature_dict[file] = 'a'

f = open("result.txt", "w")
f.write(current_time_str() + "\n")
f.write("Comparing results for " + str(len(files)) + " images.\n\n\n")

for x in range(len(files)):
    image_a = files[x]
    percent = x / len(files) * 100
    log('(' + str(round(percent, 2)) + '%) ' + 'Finding similar images for ' + image_a)
    similar_images = {}
    for y in range(x + 1, len(files)):
        image_b = files[y]
        if random.random() < 0.001:
            similar_images[y] = random.random()
    if len(similar_images) > 0:
        f.write('Similar images for ' + paths[x] + '\n')
        for image_y, val in similar_images.items():
            f.write('\t' + paths[image_y] + '  (' + str(round(val * 100, 2)) + '%)\n')
        f.write('\n\n')

f.close()
log('(100%) Completed!')
