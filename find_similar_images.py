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

import imagehash
from PIL import Image


def log(msg):
    print('[' + current_time_str() + '] ' + str(msg))


def current_time_str():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")


# path = input('Path: ')
path = 'C:\\Users\\marstan\\OneDrive\\Pictures\\Anime\\Anmi\\图'

files = []

img_exts = ['.jpg', '.jpeg', 'png']
signature_dict = {}

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        (filename, ext) = os.path.splitext(file)
        if ext in img_exts:
            log('hashing ' + file)
            full_name = os.path.join(r, file)
            key = full_name.replace(path, '').replace('\\', '', 1)
            files.append(key)
            image_hash = imagehash.average_hash(Image.open(full_name))
            signature_dict[key] = image_hash

f = open("result.txt", "w")
f.write(current_time_str() + "\n")
f.write("Comparing results for " + str(len(files)) + " images.\n\n\n")

similar_images = []

for x in range(len(files)):
    image_a = files[x]
    percent = x / len(files) * 100
    log('(' + str(round(percent, 2)) + '%) ' + 'Finding similar images for ' + image_a)
    for y in range(x + 1, len(files)):
        image_b = files[y]
        if signature_dict[image_a] - signature_dict[image_b] < 3:
            found = False
            count = 0
            for image_group in similar_images:
                if image_a in image_group and image_b in image_group:
                    found = True
                    break
                if image_a in image_group and image_b not in image_group:
                    similar_images[count].append(image_b)
                    found = True
                    break
                count += 1
            if not found:
                image_group = [image_a, image_b]
                similar_images.append(image_group)

log('(100%) Completed!')

similar_images.sort(key=lambda item: -len(item))

for image_group in similar_images:
    f.write('Similar images\n')
    count = len(image_group)
    for image in image_group:
        f.write('\t' + image + '\n')
        if '合集散图' in image and count > 1:
            os.remove(os.path.join(path, image))
            count -= 1
            log('Removed' + image)
    f.write('\n\n')

f.close()
