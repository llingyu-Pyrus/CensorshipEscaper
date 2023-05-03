from PIL import ImageGrab,Image
import random
import pyvirtualcam
import numpy

def cropImage(im,w,h,wc,hc):
    list = []
    tmp = []
    sw = w//wc
    sh = h//hc
    for i in range(hc):
        for j in range(wc):
            tmp.append(im.crop((sw*j,sh*i,sw*j+sw,sh*i+sh)))
        list.append(tmp)
        tmp = []
    return list

def getSeed(token):
    return (token*token*token)%1000000

def spliceImage(im, mapt,w,h,wc,hc):
    tmp = Image.new('RGB',(w,h),(0,0,0))
    sw = w//wc
    sh = h//hc
    for i in range(hc):
        for j in range(wc):
            tmp.paste(im[i][j],(sw*mapt[i][j][1],sh*mapt[i][j][0]))
    return tmp

def genTab(wc,hc):
    a = []
    b = []
    for i in range(hc):
        for j in range(wc):
            b.append((i,j))
        a.append(b)
        b = []
    for i in range(hc):
        random.shuffle(a[i])
    random.shuffle(a)
    return a

token = int(input('Input token: '))
w = int(input('Input width: '))
h = int(input('Input height: '))
wc = int(input(r'How many chunk do you want per line (w%wc=0) : '))
hc = int(input(r'How many chunk do you want per row (h%hc=0) : '))
fr = int(input(r'Input framerate (30 recommended) : '))

if(not (w%wc == 0) or not (h%hc == 0)):
    print('Error: chunk must be integer')
    exit()

random.seed(getSeed(token))
mapt = genTab(wc,hc)
with pyvirtualcam.Camera(width=w, height=h, fps=fr) as cam:
    print(f'Using virtual camera: {cam.device}')
    while True:
        im = ImageGrab.grab((0,0,w,h))
        a = cropImage(im,w,h,wc,hc)
        cam.send(numpy.asarray(spliceImage(a,mapt,w,h,wc,hc)))
        cam.sleep_until_next_frame()

# im = Image.open('CensorshipEscaper/1.png')
# a = cropImage(im,1900,1000,19,10)
# spliceImage(a,genTab(19,10),1900,1000,19,10).save('1.png')
# 
# for i in range(10):
#         for j in range(19):
#             a[i][j].save('{0},{1}.png'.format(str(i),str(j)))