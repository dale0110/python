import urllib
import urllib2
import time
import re
import sys

def get_jpg(url,path):
    socket = urllib2.urlopen(url)
    data = socket.read()
    with open(path, "wb") as jpg:
        jpg.write(data)
    socket.close()
    
def usage():
    print "Usage: python" + ' ' + sys.argv[0] + ' ' + "<url>"
    sys.exit()
    
def test1():

    html='''MountainMist_ZH-CN11102136834_1366x768.jpg',id:'bgDiv'''
    #url_re = re.compile(r'''{url:\w*,id''')
    #url_re = re.compile(r'''{url:[a-zA-Z0-9_///*-]*,id''')
    url_re = re.compile(r'''[a-zA-Z0-9-x_]*.jpg''')
    for  pic_url in url_re.findall(html):
        print pic_url


def download_bing_pic():
    
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
    
def download_cl_pic(url):
    
    f = urllib.urlopen(url)
    html = f.read()
    #src='http://102.imagebam.com/download/tT8uQQNEFqwdl5H_kDew7A/28622/286211832/460%281%29.jpg' 
    url_re = re.compile(r'''src='[%:.a-zA-Z0-9-x_/]*.jpg''')
    url_list = url_re.findall(html)
    #print url_list
    for pic_url in url_list:
        print pic_url[5:]
        name=time.strftime("%Y%m%d-%H%M%S", time.localtime())
        name=name+".jpg"
        urllib.urlretrieve(pic_url[5:],name)
        time.sleep(1)
    f.close()
    

def main():
    '''
    if len(sys.argv) < 2:
        usage()
    '''
    #download_cl_pic(sys.argv[1])
    download_cl_pic("http://cl.or.gs/htm_data/16/1311/975087.html")

if __name__ == "__main__":
    main()
