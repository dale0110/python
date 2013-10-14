# coding:UTF-8

import urllib
import urllib2
import codecs
from bs4 import BeautifulSoup
from sys import argv
import re,time
import logging
import urlparse
import mechanize

''' 创建一个logger ''' 
logger = logging.getLogger('mylogger')  
logger.setLevel(logging.DEBUG)  
  
''' 创建一个handler，用于写入日志文件 '''
fh = logging.FileHandler('test.log')  
fh.setLevel(logging.DEBUG)  
  
'''再创建一个handler，用于输出到控制台  '''
ch = logging.StreamHandler()  
ch.setLevel(logging.DEBUG)  
  
''' 定义handler的输出格式  '''
formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d- %(levelname)s - %(message)s')  
fh.setFormatter(formatter)  
ch.setFormatter(formatter)  
  
''' 给logger添加handler  '''
logger.addHandler(fh)  
logger.addHandler(ch)

def get_sharejs():
    url = urllib2.urlopen("http://www.sharejs.com")
    content = url.read()
    soup = BeautifulSoup(content)
    for a in soup.findAll('a',href=True):
        if re.findall('sharejs', a['href']):
            print "Found the URL:", a['href']


def get_test():
    url = ["http://www.sparkbrowser.com","http://www.adbnews.com/area51/", "http://sheldonbrown.com/web_sample1.html"]
    
    visited = [url]
    
    
    i=0
    
    while i<len(url):
    
        #Mechanize
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Firefox')]
        br.open(url[i])
    
        #BeautifulSoup
        htmlcontent = urllib.urlopen(url[i])
        soup = BeautifulSoup(htmlcontent)
    
        levelLinks = []
        linkText = [] 
        imageLinks = []
        imageAlt = []
    
        for link in br.links(text_regex=re.compile('^((?!IMG).)*$')):
            newurl = urlparse.urljoin(link.base_url, link.url)
            b1 = urlparse.urlparse(newurl).hostname
            b2 = urlparse.urlparse(newurl).path
            wholeLink = "http://"+b1+b2
            linkTxt = link.text
            linkText.append(linkTxt)
            levelLinks.append(wholeLink)
    
        for linkwimg in soup.find_all('a'):
            imgSource = linkwimg.find('img')
            if linkwimg.find('img',alt=True):
                imgLink = linkwimg['href']
                imageLinks.append(imgLink)
                imgAlt = linkwimg.img['alt']
                imageAlt.append(imgAlt)
            elif linkwimg.find('img',alt=False):
                imgLink = linkwimg['href']
                imageLinks.append(imgLink)
                imgAlt = ['No Alt']
                imageAlt.append(imgAlt)
    
        print "\n\n\n\nLinks and Text for "+b1+":\n\n"
    
        #get Mechanize Links
        for l,lt in zip(levelLinks,linkText):
            print l,"\n",lt,"\n"
    
        print "\n\n\n\nImage links and alt for "+b1+":\n\n"
    
        #get BeautifulSoup image Links & alt content
        for il,ia in zip(imageLinks,imageAlt):
            print il,"\n",ia,"\n"
    
        i+=1
  
  
def get_python():
    #specify the url you want to query
    url = "http://www.python.org"
      
    #Query the website and return the html to the variable 'page'
    page = urllib2.urlopen(url)
 
    '''
    cur_content=page.read()
    print len(cur_content)
    print cur_content)
    '''  
      
    #Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page)
      
    #to print the soup.head is the head tag and soup.head.title is the title tag
    logger.info('start head')
    print soup.head
    logger.info('end head')
 
    logger.info('start title')   
    print soup.head.title
    logger.info('end title')  
      
    #to print the length of the page, use the len function
    #print len(page)
      
    #create a new variable to store the data you want to find.
    tags = soup.findAll('a')
      
    #to print all the links
    logger.info('start tags')
    print tags
    logger.info('end tags')
      
    #to get all titles and print the contents of each title
    allTitles = soup.findAll('span', attrs = { 'class' : 'titletext' })
    for title in allTitles:
        print title.contents
        



class Translate:
    def Start(self):
        logger.info('Start ')   
        self._get_html_sourse()
        self._get_content("enc")
        self._remove_tag()
        self.print_result()

    def _get_html_sourse(self):
        word='good'
        url="http://dict.baidu.com/s?wd=%s&tn=dict" %  word
        self.htmlsourse=unicode(urllib.urlopen(url).read(),"gb2312","ignore").encode("utf-8","ignore")
        logger.info(self.htmlsourse)

    def _get_content(self,div_id):
        soup=BeautifulSoup("".join(self.htmlsourse))
        self.data=str(soup.find("div",{"id":div_id}))
        logger.info(self.dat)

    def _remove_tag(self):
        soup=BeautifulSoup(self.data)
        self.outtext=''.join([element  for element in soup.recursiveChildGenerator() if isinstance(element,unicode)])
        logger.info('_remove_tag OK')

    def print_result(self):
        for item in range(1,10):
            self.outtext=self.outtext.replace(str(item),"\n%s" % str(item))
        self.outtext=self.outtext.replace("  ","\n")
        print self.outtext




#from sharejs.com

if __name__=="__main__":
     #Translate().Start()
     #get_python()
     #get_sharejs()
     get_test()

 


