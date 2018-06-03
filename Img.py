# 将图片转化成字符画

from PIL import Image

# ascii_char =list("/\|()1{}$@B%8&WM#ZO0QLCJUYX*hkbdpqwmoahkbdpqwmzcvunxrjft[]?-_+~<>i!lI;:,\"^`'. ")
# ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

strs = {
    '1': list(' ...\',;:clodxkLO0DGEKNWMM')[::-1],
    '2': list('@#MBHA&XG893S5h1sri;:-,. '),
    '3': list('@MBHAXG89S5h1ri;:,. '),
    '4': ['@', 'w', '#', '$', 'k', 'd', 't', 'j', 'i', '.', ' '],
    '5': list(".`_-'\"^;=L~!cxIr*ZCg{9FE[R/Ydnpq#V$OMHBU")[::-1]
}

ascii_char = strs['4']
imgname = "test1.jpg"
output = "test1.txt"

width = 140
height = 80


def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0+1)/length
    return ascii_char[int(gray/unit)]

img = Image.open(imgname)
img = img.resize((width, height), Image.NEAREST)

txt = ""

for i in range(height):
    for j in range(width):
        char_ = get_char(*img.getpixel((j, i)))
        txt += char_
        print(char_, end='')
    txt += '\n'
    print()

with open(output, 'w') as f:
    f.write(txt)
