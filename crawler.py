import os
import re
import time
import urllib
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver


url = "http://blog.sina.com.cn/s/blog_70e8ec2b0102vjlq.html"

def retriveImg(url):
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


retriveImg(url)

