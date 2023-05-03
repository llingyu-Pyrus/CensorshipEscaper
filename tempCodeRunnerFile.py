import pyvirtualcam
import cv2
import numpy  
from PIL import Image

im = Image.new("RGBA", (1920,1080), (0,0,0,0))
i = 0
with pyvirtualcam.Camera(width=1920, height=1080, fmt=pyvirtualcam.PixelFormat('ABGR'), fps=30) as cam:
    print(f'Using virtual camera: {cam.device}')
    while True:
        img = cv2.cvtColor(numpy.asarray(im),cv2.COLOR_RGBA2BGRA)
        cam.send(img)
        im.putpixel((i,i),(i,i,i,i))
        i+=1
        if i == 255:
            break
        cam.sleep_until_next_frame()