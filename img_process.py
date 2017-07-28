import cv2
import os
import numpy as np

thr = 100
maxv = 255
o_kernel = np.ones((2, 2), np.uint8)
e_kernel = np.ones((1, 1), np.uint8)

def testing():
    img = cv2.imread("8.jpg", 0)
    ret, del_noise = cv2.threshold(img, thr, maxv, cv2.THRESH_BINARY)

    for i in range(1):
        del_noise = cv2.morphologyEx(del_noise, cv2.MORPH_OPEN, o_kernel)
        del_noise = cv2.morphologyEx(del_noise, cv2.MORPH_CLOSE, e_kernel)

    cv2.namedWindow('origin', 0)
    cv2.imshow('origin', img)
    cv2.namedWindow('after', 0)
    cv2.imshow('after', del_noise)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def noiseless():
    path = os.path.join(os.getcwd(), "noise")
    for img_name in os.listdir(path):
        try:
            img = cv2.imread(os.path.join(path, img_name), 0)
            ret, del_noise = cv2.threshold(img, thr, maxv, cv2.THRESH_BINARY)
            del_noise = cv2.morphologyEx(del_noise, cv2.MORPH_OPEN, o_kernel)
            del_noise = cv2.morphologyEx(del_noise, cv2.MORPH_CLOSE, e_kernel)
            cv2.imwrite(os.path.join(path, img_name), del_noise)
            print "Processing {0} complete!".format(img_name)
        except Exception as e:
            print e

noiseless()


