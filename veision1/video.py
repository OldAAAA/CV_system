import numpy as np
import os
from time import sleep

import cv2
from PIL import Image


def generetor():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()

        imgRGB = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
        r, buf = cv2.imencode(".jpg", imgRGB)
        bytes_image = Image.fromarray(np.uint8(buf)).tobytes()

        # frame = cv2.imread("static/media/"+str(i)+".jpg",1)
        # if cv2.waitKey(10) == 27:
        #     break
        # print("static/media/"+str(i)+".jpg")  # 获取当前工作目录路径
        # print(frame)
        # print(i)
        # cv2.imshow("frame",frame)
        # cv2.waitKey(1000)
        # cv2.destroyAllWindows()
        yield (b'Content-Type:image/jpeg\r\n\r\n' + bytes_image + b'\r\n--frame')
        # yield (b'--frame\r\n'+b'Content-Type:image/jpeg\r\n\r\n' + bytes_image + b'\r\n--frame')
        # yield (b'--frame\r\n'
        #        b'Content-Type:image/jpeg\r\n\r\n' + bytes(frame) + b'\r\n\r\n')

# frame = cv2.imread("1.jpg")
# # if cv2.waitKey(10) == 27:
# #     break
# cv2.imshow("frame",frame)
# cv2.waitKey(10000)


# generetor()
