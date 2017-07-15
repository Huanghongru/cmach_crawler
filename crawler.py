# ! coding: utf-8
import os
import re
import time
import codecs
import urllib
import chardet
import urllib2
import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver

def retriveImg_sinablog(url):
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

def retriveImg_zitiweb(url):
    """
    This function crawl a shufa generation web
    :param url: http://www.zitiweb.com/mj.php
    :return: retrieved images were stored in /zitiweb
    """
    real_url = "http://www.zitiweb.com"
    path = os.path.join(os.getcwd(), "zitiweb")

    with open("hanzi.txt", "r") as hf:
        lines = hf.readlines()
        for i in range(1041, len(lines)):
            try:
                char_code = "%".join(['']+lines[i].split()[2:5])
                req = urllib2.Request(url, "text="+char_code)
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

if __name__ == '__main__':
    url = "http://www.zitiweb.com/mj.php"
    retriveImg_zitiweb(url)


# crawl to 1038th character



