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


def filter_withoutMSE(img_name, path):
    """
    Filter without MSE, mainly to determine whether it is a blank picture
    :param img_name
    :return:
    """
    img = cv2.imread(os.path.join(path, img_name))
    subimg = img.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if np.sum(img[i, j], dtype=np.int) > sum_th:
                subimg[i, j] = np.array([255, 255, 255])
    return subimg


def is_blank(img, path):
    return (void_img == filter_withoutMSE(img, path)).all()


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
                        tf.write("{0}.png\t".format(i*8+j+1))
                        print "Adding {0}.png to tag:{1}".format(i*8+j, Tag)
                tf.write('\n')
        except Exception as e:
            print e


def filt_redline(origin_file_name, filterd_file_name):
    des_path = os.path.join(os.getcwd(), filterd_file_name)
    path = os.path.join(os.getcwd(), origin_file_name)
    images = os.listdir(path)
    for img_name in images:
        try:
            if os.path.exists(os.path.join(des_path, img_name)):
                print "{0} already exists".format(img_name)
                continue
            img = cv2.imread(os.path.join(path, img_name))
            filted_img = filter_withMSE(img)
            cv2.imwrite(os.path.join(des_path, img_name), filted_img)
            print "Complete removing red line in {0}".format(img_name)
        except Exception as e:
            print e

def filter_white(file_name):
    """
    Task assigned by Master Yi, and further filtering is needed
    :return:
    """
    def white_rate(img_name, lpath):
        img = cv2.imread(os.path.join(lpath, img_name))
        sum = 0
        s = 40468500.0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                sum += img[i, j].sum()
        return sum/s

    lpath = os.path.join(os.getcwd(), file_name)
    white_th = 0.9995
    for img in os.listdir(lpath):
        if white_rate(img, lpath) > white_th:
            os.remove(os.path.join(lpath, img))
            print "{0} is a white image!!".format(img)
        else:
            print "{0} is a valid image!!".format(img)


def label():
    utf = []
    with open("tag.txt", "r") as tf:
        for line in tf.readlines():
            utf.append(line.split()[0])

    lpath = os.path.join(os.getcwd(), "ztw")
    with open("label.txt", "a") as lf:
        for img_name in os.listdir(lpath):
            lf.write(utf[(int(img_name[:-4])-1)/8]+' ')


def copyImg(img, sourceDir, targetDir):
    with open(os.path.join(sourceDir, img), "rb") as oif:
        with open(os.path.join(targetDir, img), "wb") as nf:
            nf.write(oif.read())

def getCaligrapher(num, targetDir):
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)

    with open("tag.txt", "r") as tf:
        for line in tf.readlines():
            if not os.path.exists(os.path.join(targetDir, "label.txt")):
                f = open("label.txt", "w")
                f.close()
            with open(os.path.join(targetDir, 'label.txt'), "a") as lf:
                lf.write(line.split()[0] + ' ')

    spath = os.path.join(os.getcwd(), "ztw")
    tpath = os.path.join(os.getcwd(), targetDir)
    for img in os.listdir(spath):
        if (int(img[:-4])-1)%8 == num:
            copyImg(img, spath, tpath)
            print "copy {} ".format(img)

if __name__ == '__main__':
    # spath = os.path.join(os.getcwd(), "ztw")
    # tpath = os.path.join(os.getcwd(), "wxz")
    # with open(os.path.join(spath, "1.png"), "rb") as sf:
    #     with open(os.path.join(tpath, "1.png"), "wb") as tf:
    #         tf.write(sf.read())
    getCaligrapher(7, "shzsjt")




