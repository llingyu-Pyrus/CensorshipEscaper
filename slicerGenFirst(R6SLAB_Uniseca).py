from PIL import ImageGrab, Image
import random
import pyvirtualcam
import numpy
import sys
from numba import jit

@jit
def crop_image(im, w, h, wc, hc):
    lst = []
    sw = w // wc
    sh = h // hc
    for i in range(hc):
        for j in range(wc):
            lst.append(im.crop((sw*j, sh*i, sw*j+sw, sh*i+sh)))
    return lst


def get_seed(token):
    return (token * token * token) % 1000000

@jit
def splice_image(im, mapt, w, h, wc, hc):
    sw = w // wc
    sh = h // hc
    new_im = Image.new('RGB', (w, h), (0, 0, 0))
    for i in range(hc):
        for j in range(wc):
            new_im.paste(im[i*wc+j], (sw*mapt[i][j][1], sh*mapt[i][j][0]))
    return new_im


def gen_tab(wc, hc):
    a = [(i, j) for i in range(hc) for j in range(wc)]
    random.shuffle(a)
    b = [a[i:i+wc] for i in range(0, len(a), wc)]
    random.shuffle(b)
    return b


def main():
    token = int(input('Input token: '))
    w = int(input('Input width: '))
    h = int(input('Input height: '))
    wc = int(input(r'How many chunks do you want per line (w%wc=0) : '))
    hc = int(input(r'How many chunks do you want per row (h%hc=0) : '))
    fr = int(input(r'Input framerate (30 recommended) : '))

    if not (w % wc == 0) or not (h % hc == 0):
        print('Error: chunk must be integer')
        sys.exit()

    random.seed(get_seed(token))
    mapt = gen_tab(wc, hc)

    with pyvirtualcam.Camera(width=w, height=h, fps=fr, print_fps=True) as cam:
        print(f'Using virtual camera: {cam.device}')
        while True:
            im = ImageGrab.grab((0, 0, w, h))
            lst = crop_image(im, w, h, wc, hc)
            cam.send(numpy.asarray(splice_image(lst, mapt, w, h, wc, hc)))
            cam.sleep_until_next_frame()


if __name__ == '__main__':
    main()
