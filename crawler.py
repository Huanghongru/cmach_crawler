# coding=utf-8
import os
import urllib
import urllib2
import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def retrieveImg_sinablog(url):
    """
    This function crawl a sina blog full of handwritten masterpiece by Yingzhang Tian
    :param url: the sina blog url: http://blog.sina.com.cn/s/blog_70e8ec2b0102vjlq.html
    :return: retrieved images were stored in /tyz
    """
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content, "lxml")
    images = soup.findAll('img', {'alt': u"\u7530\u82f1\u7ae0\u2014\u5355\u5b571",
                                  'title': u"\u7530\u82f1\u7ae0\u2014\u5355\u5b571"})

    for i in range(220, len(images)):
        path = os.path.join(os.getcwd(), "tyz")
        imgurl = images[i].get("real_src")
        try:
            urllib.urlretrieve(imgurl, path+"\\{0}.jpg".format(i+1))
            print "Download image complete!!    Total: {0}".format(i+1)
        except Exception as e:
            print e

def retrieveImg_zitiweb(char_list, stored_file_name):
    """
    This function crawl a shufa generation web
    :param url: http://www.zitiweb.com/mj.php
    :return: retrieved images were stored in /zitiweb
    """
    url = "http://www.zitiweb.com/mj.php"
    real_url = "http://www.zitiweb.com"
    path = os.path.join(os.getcwd(), stored_file_name)

    for i in range(len(char_list)):
        try:
            req = urllib2.Request(url, "text="+char_list[i])
            response = urllib2.urlopen(req)
            content = response.read()
            soup = BeautifulSoup(content, "lxml")
            images = soup.findAll('img')
            for j in range(1, len(images) - 1):
                img_name = path + "\\{0}.png".format(i*8+j)
                if os.path.exists(img_name):
                    print "Image already exists!"
                    continue
                img_url = urlparse.urljoin(real_url, images[j].get('src'))
                urllib.urlretrieve(img_url, img_name)
                print "Retrieved character {0} with mode {1}".format(i, i*8+j)
        except Exception as e:
            print e


def retrieveImg_52maobizi(calligrapher, type, stored_dir_name, attrib, img_name, maxNum=2000):
    """
    This function crawl a calligraphy generation web
    :param calligrapher:        an str specifies the calligrapher, the calligrapher-value pair are as follows:
                        楷书：{‘柳公权毛笔书法字体’：    185，   ’颜真卿楷书毛笔书法字体‘：196，  ’欧体楷书毛笔字体‘：  187}
                        行书：{’王羲之毛笔行书书法字体‘：181，    ’八大山人毛笔字体‘：     183， ’米芾行书毛笔字体‘：   188,
                              '李旭科':               184,    '叶根友':              220,   '郑板桥':           251,
                              '向佳红':               218,    '金梅':                210,   '蔡云汉':           214,
                              '段宁':                 229,    '良怀':               233,    '孙中山':          234,
                              '舒同':                 235,    '赵孟頫':              186,    '钟齐':           213}
    :param type:                a string specifies the calligraphy type, must be one of the following:
                                [kaishu, caoshu, xingshu, xingkai, lishu, weibei]
    :param stored_file_name:    file where retrieved images were stored
    :param attrib:              a list of the attribution of the retrieved img [size, width, height]
    :param img_name:            a str specifies the stored_image name
    :param maxNum:              an int specifies the max crawled num of images
    :return:
    """
    if not os.path.exists(stored_dir_name):
        os.mkdir(stored_dir_name)

    # get all utf code
    utf = []
    with open("tag.txt", "r") as tf:
        for line in tf.readlines():
            utf.append(line.split()[0])

    # set character attribution
    url = "http://www.52maobizi.com/"+type
    driver = webdriver.Chrome()
    driver.get(url)

    select = Select(driver.find_element_by_id('FontInfoId'))
    select.select_by_value(calligrapher)

    font_size = driver.find_element_by_name("FontSize")
    font_size.clear()
    font_size.send_keys(attrib[0])

    img_w = driver.find_element_by_name("ImageWidth")
    img_w.clear()
    img_w.send_keys(attrib[1])

    img_h = driver.find_element_by_name("ImageHeight")
    img_h.clear()
    img_h.send_keys(attrib[2])

    # retrieve image for corresponding utf-8
    for i in range(0, maxNum):
        char_dir = os.path.join(stored_dir_name, str(i))
        if not os.path.exists(char_dir):
            os.mkdir(char_dir)

        try:
            char = driver.find_element_by_name("Content")
            char.clear()
            char.send_keys(eval("u'\u{0}'".format(utf[i])))

            driver.find_element_by_id("btnOnline").click()
            content = driver.page_source

            soup = BeautifulSoup(content, "lxml")
            img_src = soup.findAll("img", {"id": "imgResult"})[0].get('src')

            stored_img_name = img_name+'.png'
            if not os.path.exists(os.path.join(char_dir, stored_img_name)):
                urllib.urlretrieve(img_src, os.path.join(char_dir, stored_img_name))
                print "{0}. retrieve {1}".format(i, stored_img_name)
            else:
                print "{0}. image {1} already exists.".format(i, stored_img_name)
        except Exception as e:
            print e


if __name__ == '__main__':
    # calligraphers = ['185', '196', '187']
    # type = 'kaishu'
    # stored_file_name = "standard"
    # attrib = ['75', '128', '128']
    # retrieveImg_52maobizi(calligraphers[2], type, stored_file_name, attrib, '2')

    art_clp = ['181', '183', '188', '184', '220',
               '251', '218', '210', '214', '229',
               '233', '234', '235']
    type = "xingshu"
    stored_file_name = "art"
    attrib = ['75', '128', '128']
    for i in range(7, len(art_clp)):
        retrieveImg_52maobizi(art_clp[i], type, stored_file_name, attrib, str(i))

# stop at 8.png 1000, continue 1001