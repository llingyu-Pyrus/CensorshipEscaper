# -*- coding:UTF-8 -*-
import cv2
import random
from numba import jit
from PIL import Image
import numpy

def get_seed(token):
    return (token * token * token) % 1000000

def gen_tab(wc, hc):
    a = [(i, j) for i in range(hc) for j in range(wc)]
    random.shuffle(a)
    b = [a[i:i+wc] for i in range(0, len(a), wc)]
    random.shuffle(b)
    return b

@jit
def crop_image(im, w, h, wc, hc):
    lst = []
    sw = w // wc
    sh = h // hc
    for i in range(hc):
        for j in range(wc):
            lst.append(im.crop((sw*j, sh*i, sw*j+sw, sh*i+sh)))
    return lst

@jit
def splice_image(im, mapt, w, h, wc, hc):
    new_lst = []
    for i in range(hc):
        row_lst = []
        for j in range(wc):
            row_lst.append(im[i*wc+j])
        new_lst.append(row_lst)
    
    new_im = Image.new('RGB', (w, h), (0, 0, 0))
    for i in range(hc):
        for j in range(wc):
            new_im.paste(new_lst[mapt[i][j][0]][mapt[i][j][1]], (j*w//wc, i*h//hc))
    return new_im

cap = cv2.VideoCapture('rtmp://localhost:1935/live/movie')
fps = cap.get(cv2.CAP_PROP_FPS)

b = int(input('Chunk per line: '))
a = int(input('Chunk per row: '))
token = int(input("Token: "))
random.seed(get_seed(token))

mapt = gen_tab(b, a)
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    parts = crop_image(Image.fromarray(frame),frame.shape[1],frame.shape[0],b,a)
    
    # print(parts)
    result = numpy.asarray(splice_image(parts, mapt, frame.shape[1], frame.shape[0],b,a))
    
    try:
        cv2.imshow('Decoded', result)
    except:
        None
        
    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
