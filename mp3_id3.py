import os
import sys

import eyed3
import eyed3.id3.frames

my_path = 'D:\\Music\\English\\'

img_exts = ['.mp3']


def process(file):
    try:
        audiofile = eyed3.load(file)
        if len(audiofile.tag.images) is 1:
            imageinfo = audiofile.tag.images[0]
            if imageinfo.picture_type is 6:
                print(file)
                imagedata = imageinfo.image_data
                audiofile.tag.images.remove('6')
                audiofile.tag.images.set(3, imagedata, imageinfo.mime_type)
                audiofile.tag.save()
    except:
        pass


# r=root, d=directories, f = files
for r, d, f in os.walk(my_path):
    for file in f:
        (filename, ext) = os.path.splitext(file)
        if ext in img_exts:
            full_name = os.path.join(r, file)
            process(full_name)
