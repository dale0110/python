#!/usr/bin/python
#-*-coding:utf-8-*-
import os, re, sys, time
import urllib2
import urlparse
from urlparse import urljoin


#定义全局变量
first_url='http://www.wenxuewu.com/files/article/html/111/111306/3940183.html'
save_name='a.txt'
save_fd=0

def gettxt(html_content):
    #title_re = re.compile(r'<div id="title1"><h1>[.]*[\x80-\xff]+[ \t]+')
    #将所有中文字符搜索出来
    #title_re = re.compile(r'''[\x80-\xff]+''')
    title_re = re.compile(r'''&nbsp;&nbsp;&nbsp;&nbsp;[\x80-\xff ]*''')
    txt_title = title_re.findall(html_content)
    #print txt_title
    print len(txt_title)
    for txt in txt_title:
        #str = "%s ( %d ): %s\n" % (f, i, c)
        #print txt
        #global save_fd
        save_fd.write(txt[24:]+'\n')




#处理一个网页内容
def get_html(cur_url):
    cur_html = urllib2.urlopen(cur_url)
    cur_content=cur_html.read()
    print len(cur_content)

    #保持网页正文内容
    gettxt(cur_content)

    #获取下一个链接链接关键词
    #<a href="/files/article/html/111/111306/8308329.html">下一页</a>
    link_regex = re.compile(r'<a href="[1-9]+\.html">下一页')
    next_link = link_regex.finditer(cur_content)
    print len(next_link)
    #处理下一个链接
    get_html(next_link)
    
    root_html.close()

def main():
    cu_dir = os.getcwd()
    save_fd = open(save_name,'w')
    get_html(first_url)
    save_fd.close()

if __name__ == '__main__':  
        main()
#    getsublinktxt('http://www.wenxuewu.com/files/article/html/111/111306/3940214.html')
