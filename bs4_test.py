# coding:utf-8

import urllib2

import logging  

from bs4 import BeautifulSoup
  
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
  

 
#specify the url you want to query
url = "http://www.python.org"
 
#Query the website and return the html to the variable 'page'
page = urllib2.urlopen(url)
 
#import the Beautiful soup functions to parse the data returned from the website

 
#Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page)
 
#to print the soup.head is the head tag and soup.head.title is the title tag
print soup.head
print soup.head.title
 
#to print the length of the page, use the len function
#print len(page)
 
#create a new variable to store the data you want to find.
tags = soup.findAll('a')
 
logger.info('tag')  
#to print all the links
print tags
 

logger.info('title')  
#to get all titles and print the contents of each title
titles = soup.findAll('span', attrs = { 'class' : 'titletext' })
for title in titles:
    print title.contents
