import urllib
import urllib2
import time
import re

def get_jpg(url,path):
    socket = urllib2.urlopen(url)
    data = socket.read()
    with open(path, "wb") as jpg:
        jpg.write(data)
    socket.close()
    
def test1():

    html='''MountainMist_ZH-CN11102136834_1366x768.jpg',id:'bgDiv'''
    #url_re = re.compile(r'''{url:\w*,id''')
    #url_re = re.compile(r'''{url:[a-zA-Z0-9_///*-]*,id''')
    url_re = re.compile(r'''[a-zA-Z0-9-x_]*.jpg''')
    for  pic_url in url_re.findall(html):
        print pic_url


def main():
    
    url = 'http://www.bing.com'
    f = urllib.urlopen(url)
    html = f.read()
    #html='''{url:'http://s.cn.bing.net/az/hprichbg/rb/MountainMist_ZH-CN11102136834_1366x768.jpg',id:'bgDiv'''
    url_re = re.compile(r'''{url:'[:.a-zA-Z0-9-x_/]*.jpg''')
    url_list = url_re.findall(html)
    print url_list
    for pic_url in url_list:
        print pic_url[6:]
        urllib.urlretrieve(pic_url[6:],"test.jpg")
    f.close()

if __name__ == "__main__":
    main()
