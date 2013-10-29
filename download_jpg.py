import urllib
import urllib2
import time

def get_jpg(url,path):
    socket = urllib2.urlopen(url)
    data = socket.read()
    with open(path, "wb") as jpg:
        jpg.write(data)
    socket.close()

def main():
    url = 'http://www.bing.com'
    f = urllib.urlopen(url)
    html = f.read()
    f.close()
    a = html[html.index('//fd//hpk2'):]
    data = a[:a.index('/',id:')]
    url = data.replace('//', '')
    url = 'http://www.bing.com'+url
    name=time.strftime("%Y%m%d", time.localtime())
    name=name+".jpg"
    urllib.urlretrieve(url,name)

if __name__ == "__main__":
    main()
