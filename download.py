import os
import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard

def download():
    m = PyMouse()
    k = PyKeyboard()
    path = os.path.join(os.getcwd(), "cpbooks_sfa")

    curlen = os.listdir(path)
    sleep_time = 3
    dl_x, dl_y = 833L, 182L
    chrome_x, chrome_y = 116L, 839L

    with open("copybook_sfa_bdcloudAndCode.txt", "r") as cpfile:
        pages = cpfile.readlines()
        for i in range(len(pages)):
            info = pages[i].split('\t')
            page, code = info[0], info[1]

            m.click(chrome_x, chrome_y) # Open Chorme
            time.sleep(sleep_time)

            k.type_string(page+"\n")    # Input page url
            time.sleep(sleep_time)

            print "Downloading page {0} with code:{1}...".format(page, code), i+1,
            if code == "NoCode":
                m.click(dl_x, dl_y)
                time.sleep(sleep_time**2)
            else:
                k.type_string(code+"\n")
                time.sleep(sleep_time)
                m.click(dl_x, dl_y)
                time.sleep(sleep_time**2)

            if len(os.listdir(path)) == curlen:
                with open("failed_page.txt", "wa") as fp:
                    fp.write(page+'\t'+code+'\n')
                print "Page failed..."
            else:
                suffix = os.listdir(path)[-1][-10:]
                while suffix == "crdownload":
                    time.sleep(1)
                    suffix = os.listdir(path)[-1][-10:]
                print "Download completed!!!"

download()
