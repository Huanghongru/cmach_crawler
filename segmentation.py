import os
import cv2
import numpy as np

sum_th = 220
mse_th = 10.0
img = cv2.imread('2.png')
path = os.path.join(os.getcwd(), "zitiweb")
void_img = np.tile(np.array([255, 255, 255]), (230, 230, 1))


def mse(tensor):
    """
    Calculate the mean square error of a vector to determine whether it is a red line
    :param tensor: a ndarray input
    :return: mse
    """
    return ((tensor-tensor.mean())**2).mean()


def filter_withMSE(img):
    """
    Filt out the red line with MSE, it can make the image smooth
    :param img:
    :return: filted image
    """
    subimg = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if np.sum(img[i, j], dtype=np.int) > sum_th and mse(img[i, j]) > mse_th:
                subimg[i, j] = np.array([255, 255, 255])
    return subimg


def filter_withoutMSE(img):
    """
    Filter without MSE, mainly to determine whether it is a blank picture
    :param img:
    :return:
    """
    subimg = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if np.sum(img[i, j], dtype=np.int) > sum_th:
                subimg[i, j] = np.array([255, 255, 255])
    return subimg


def is_blank(img):
    return (void_img == filter_withoutMSE(img)).all()


def get_voidImg_list():
    images = os.listdir(path)
    for img_name in images:
        img = cv2.imread(os.path.join(path, img_name))
        if is_blank(img):
            print "{0} is a blank image!".format(img_name)
            with open("void_list.txt", "a") as vl:
                vl.write(img_name+'\t')


def tag():
    """
    Tag image with its correspondent character
    :return:
    """
    with open("void_list.txt", "r") as vl:
        blank_images = vl.readline().split('\t')

    with open("hanzi.txt", "r") as hf:
        lines = hf.readlines()

    for i in range(len(lines)):
        try:
            Tag = lines[i].split()[1]
            with open("tag.txt", "a") as tf:
                tf.write(Tag+'\t')
                for j in range(8):
                    if "{0}.png".format(i*8+j) in blank_images:
                        print "{0}.png is a void image".format(i*8+j)
                        continue
                    else:
                        tf.write("{0}.png\t".format(i*8+j))
                        print "Adding {0}.png to tag:{1}".format(i*8+j, Tag)
                tf.write('\n')
        except Exception as e:
            print e


def filt_redline():
    with open("void_list.txt", "r") as vl:
        blank_images = vl.readline().split('\t')

    des_path = os.path.join(os.getcwd(), "ztw")
    images = os.listdir(path)
    for img_name in images:
        try:
            if img_name in blank_images:
                print "{0} is a void image".format(img_name)
                continue
            if os.path.exists(os.path.join(des_path, img_name)):
                print "{0} already exists".format(img_name)
                continue
            img = cv2.imread(os.path.join(path, img_name))
            filted_img = filter_withMSE(img)
            cv2.imwrite(os.path.join(des_path, img_name), filted_img)
            print "Complete removing red line in {0}".format(img_name)
        except Exception as e:
            print e

filt_redline()

# cv2.namedWindow('origin')
# cv2.imshow('origin', img)
# cv2.namedWindow('after1')
# cv2.imshow('after1', filter_withMSE(img))
# cv2.namedWindow('after2')
# cv2.imshow('after2', filter_withoutMSE(img))
# cv2.waitKey(0)
# cv2.destroyAllWindows()


