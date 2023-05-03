import pyvirtualcam
import cv2
import random
import numpy,pyvirtualcam,time

list = []
tmp = []
for i in range(100):
    for j in range(100):
        tmp.append((i,j))
    list.insert(i,tmp)
    tmp = []

print(list[1][0])

# im = Image.open('Project_C8pFucker/1.png')
# a = cropImage(im)
# 
# for i in range(100):
#         for j in range(100):
#             a[i][j].save('{0},{1}.png'.format(str(i),str(j)))


# im = Image.open('Project_C8pFucker/1.png')
# a = cropImage(im)
# for i in range(100):
#     random.shuffle(a[i])
# random.shuffle(a)
# spliceImage(a).save('1.png')


# with pyvirtualcam.Camera(width=w, height=h, fps=fr, print_fps=True) as cam:
#     print(f'Using virtual camera: {cam.device}')
#     while True:
#         im = ImageGrab.grab((0,0,w,h))
#         a = cropImage(im,w,h,wc,hc)
#         cam.send(numpy.asarray(spliceImage(a,mapt,w,h,wc,hc)))
#         cam.sleep_until_next_frame()

# im = Image.open('CensorshipEscaper/1.png')
# a = cropImage(im,1900,1000,19,10)
# spliceImage(a,genTab(19,10),1900,1000,19,10).save('1.png')
# 
# for i in range(10):
#         for j in range(19):
#             a[i][j].save('{0},{1}.png'.format(str(i),str(j)))
