from PIL import Image

im = Image.open('C:/Users/david/Desktop/a.png')
rgb_im = im.convert('RGB')
r, g, b = rgb_im.getpixel((1, 1))

print(im.size[0], im.size[1])
print(im.size[0] * im.size[1])
countmap = {}
locmap = {}

for w in range(im.size[0]):
    for h in range(im.size[1]):
        r, g, b = rgb_im.getpixel((w, h))
        if r == 0 and g == 0 and b == 0:
            continue
        s = '%s %s %s' % (r, g, b)
        if s in countmap:
            countmap[s] += 1
        else:
            countmap[s] = 1
        locmap[s] = '%s, %s' % (w, h)

for k in countmap:
    print(k + ':' + str(countmap[k]))
