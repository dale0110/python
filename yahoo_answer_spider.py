#!/usr/bin/python
#-*-coding:utf-8-*-

# 简易采集爬虫
#    1.采集Yahoo!Answers，parseData函数修改一下，可以采集任何网站
#    2.需要sqlite3或者pysqlite支持
#    3.可以在DreamHost.com空间上面运行
#    4.可以修改User-Agent冒充搜索引擎蜘蛛
#    5.可以设置暂停的时间，控制采集速度
#    6.采集Yahoo会被封IP数小时，所以这个采集用处不大
# Author: Lukin<mylukin@gmail.com>
# Date  : 2008-09-25

# 导入采集需要用到的模块
import re, sys, time
import httplib, os.path as osp
from urlparse import urlparse

# 执行采集 
def collect(url="http://answers.yahoo.com/"):
   global dl,error,headers; R = 0
   print "GET:",url
   urls = urlparse(url); path = urls[2];
   if urls[4]!='' : path += '?' + urls[4]
   dl.request(method="GET", url=path, headers=headers); rs = dl.getresponse()
   if rs.status==200 :
       R = parseData(rs.read(),url);
   else :
       print "3 seconds, try again ..."; time.sleep(3)
       dl.request(method="GET", url=path, headers=headers); rs = dl.getresponse()
       if rs.status==200 :
           R = parseData(rs.read(),url);
       else :
           print "3 seconds, try again ..."; time.sleep(3)
           dl.request(method="GET", url=path, headers=headers); rs = dl.getresponse()
           if rs.status==200 :
               R = parseData(rs.read(),url);
           else :
               print "Continue to collect ..."
               R = 3
   # 更新记录
   updateOneUrl(url,R)
   # 返回结果
   return R

# 处理采集到的数据
def parseData(html,url):
   global dl,conn; R = 2;
   c = conn.cursor()
   # 格式化html代码
   format = formatURL(clearBlank(html),url)
   # 取出所有的连接
   urls = re.findall(r'''(<a[^>]*?href="([^"]+)"[^>]*?>)|(<a[^>]*?href='([^']+)'[^>]*?>)''',format,re.I)
   if urls != None :
       i = 0
       # 循环所有的连接
       for regs in urls :
           # 得到一个单一的url
           sUrl = en2chr(regs[1].strip())
           # 判断url是否符合规则，符合，则插入数据库
           if re.search('http(.*?)/(dir|question)/index(.*?)',sUrl,re.I) != None :
               if re.search('http(.*?)/dir/index(.*?)',sUrl,re.I) != None:
                   if sUrl.find('link=list') == -1 and sUrl.find('link=over') == -1 :
                       sUrl+= '&link=over'
                   else:
                       sUrl = sUrl.replace('link=list','link=over')
               if sUrl[-11:]=='link=mailto' : continue
       if i>0 : print "Message: %d get a new URL." % (i,)
   
   # 截取数据
   if re.search('http(.*)/question/index(.*)',url,re.I) != None :
       sortfoot = 0
       # 自动创建分类和分类关系
       guide  = sect(format,'<ol id="yan-breadcrumbs">','</ol>','(<li>(.*?)Home(.*?)</li>)')
       aGuide = re.findall('<a[^>]*href="[^"]*"[^>]*>(.*?)</a>',guide,re.I)
       if aGuide != None :
           sortname = ""
           for sortname in aGuide :
               sortname = sortname.strip()
               sortpath = en2path(sortname)
               # 查询分类是否存在
               c.execute('SELECT [sortid],[sortname] FROM [sorts] WHERE [sortpath]=? LIMIT 0,1;',(sortpath,))
               row = c.fetchone();
               # 分类不存在，添加分类
               if row==None : 
                   c.execute('INSERT INTO [sorts]([sortname],[sortpath],[sortfoot])VALUES(?,?,?);',(sortname,sortpath,sortfoot))
                   sortfoot = c.lastrowid
               else:
                   sortfoot = row[0]
           # 标题
           title = sect(format,'<h1 class="subject">','</h1>')
           # 最佳答案
           BestAnswer = sect(format,'(<h2><span>Best Answer</span>(.*?)</h2>(.*?)<div class="content">)','(</div>)')
           # 最佳答案不存在，则不采集
           if BestAnswer != None :
               # 文章路径
               path = en2path(sortname + '-' + title.strip())
               # 问题
               adddata = sect(format,'<div class="additional-details">','</div>')
               content = sect(format,'(<h1 class="subject">(.*?)<div class="content">)','(</div>)')
               if adddata != None : content += '<br/>' + adddata
               # 其他回答
               OtherAnswer = ''
               for regs in re.findall('<div class="qa-container">(.+?)<div class="utils-container">',format):
                   if regs.find('<h2>') == -1 and regs.find('</h2>') == -1 :
                       a1 = sect(regs,'<div class="content">','</div>')
                       a2 = sect(regs,'<div class="reference">','</div>')
                       OtherAnswer+= '<div class="oAnswer">' + a1
                       if a2 != None : OtherAnswer+= '<div class="reference">' + a2 + '</div>'
                       OtherAnswer+= '</div>'
               
               # 判断采集成功
               if title != None and content != None :
                   # 将数据写入到数据
                   try :
                       c.execute('INSERT INTO [article]([sortid],[title],[path],[question],[banswer],[oanswer])VALUES(?,?,?,?,?,?);',(sortfoot,title,path,content,BestAnswer,OtherAnswer))
                       print "Message：%s.html" % (path,)
                       R = 1
                   except sqlite.IntegrityError :
                       pass
   # 提交写入数据库
   conn.commit(); c.close()
   return R
   
# 取得一条URL
def getOneUrl():
   global conn; c = conn.cursor()
   c.execute('SELECT [curl] FROM [collect] WHERE [state] IN(0,3) LIMIT 0,1;')
   row = c.fetchone(); c.close()
   if row==None : return ""
   return row[0].encode('utf-8')

# 更新一条记录的状态
def updateOneUrl(url,state):
   global conn; c = conn.cursor()
   c.execute('UPDATE [collect] SET [state]=? WHERE [curl]=?;',(state,url))
   conn.commit(); c.close()

# 清除html代码里的多余空格
def clearBlank(html):
   if len(html) == 0 : return ''
   html = re.sub('\r|\n|\t','',html)
   while html.find("  ")!=-1 or html.find('&nbsp;')!=-1 :
       html = html.replace('&nbsp;',' ').replace('  ',' ')
   return html

# 格式化url
def formatURL(html,url):
   urls = re.findall('''(<a[^>]*?href="([^"]+)"[^>]*?>)|(<a[^>]*?href='([^']+)'[^>]*?>)''',html,re.I)
   if urls == None : return html
   for regs in urls :
       html = html.replace(regs[0],matchURL(regs[0],url))
   return html

# 格式化单个url
def matchURL(tag,url):
   urls = re.findall('''(.*)(src|href)=(.+?)( |/>|>).*|(.*)url\(([^\)]+)\)''',tag,re.I)
   if urls == None :
       return tag
   else :
       if urls[0][5] == '' :
           urlQuote = urls[0][2]
       else:
           urlQuote = urls[0][5]

   if len(urlQuote) > 0 :
       cUrl = re.sub('''['"]''','',urlQuote)
   else :
       return tag

   urls = urlparse(url); scheme = urls[0];
   if scheme!='' : scheme+='://'
   host = urls[1]; host = scheme + host
   if len(host)==0 : return tag
   path = osp.dirname(urls[2]);
   if path=='/' : path = '';
   if cUrl.find("#")!=-1 : cUrl = cUrl[:cUrl.find("#")]
   # 判断类型
   if re.search('''^(http|https|ftp):(//|\\\\)(([\w/\\\+\-~`@:%])+\.)+([\w/\\\.\=\?\+\-~`@':!%#]|(&amp;)|&)+''',cUrl,re.I) != None :
       # http开头的url类型要跳过
       return tag
   elif cUrl[:1] == '/' :
       # 绝对路径
       cUrl = host + cUrl
   elif cUrl[:3]=='../' :
       # 相对路径
       while cUrl[:3]=='../' :
           cUrl = cUrl[3:]
           if len(path) > 0 :
               path = osp.dirname(path)
   elif cUrl[:2]=='./' :
       cUrl = host + path + cUrl[1:]
   elif cUrl.lower()[:7]=='mailto:' or cUrl.lower()[:11]=='javascript:' :
       return tag
   else :
       cUrl = host + path + '/' + cUrl
   R = tag.replace(urlQuote,'"' + cUrl + '"')
   return R

# html代码截取函数
def sect(html,start,end,cls=''):
   if len(html)==0 : return ;
   # 正则表达式截取
   if start[:1]==chr(40) and start[-1:]==chr(41) and end[:1]==chr(40) and end[-1:]==chr(41) :
       reHTML = re.search(start + '(.*?)' + end,html,re.I)
       if reHTML == None : return 
       reHTML = reHTML.group()
       intStart = re.search(start,reHTML,re.I).end()
       intEnd = re.search(end,reHTML,re.I).start()
       R = reHTML[intStart:intEnd]
   # 字符串截取
   else :
       # 取得开始字符串的位置
       intStart = html.lower().find(start.lower())
       # 如果搜索不到开始字符串，则直接返回空
       if intStart == -1 : return 
       # 取得结束字符串的位置
       intEnd = html[intStart+len(start):].lower().find(end.lower())
       # 如果搜索不到结束字符串，也返回为空
       if intEnd == -1 : return 
       # 开始和结束字符串都有了，可以开始截取了
       R = html[intStart+len(start):intStart+intEnd+len(start)]
   # 清理内容
   if cls != '' :
       R = clear(R,cls)
   # 返回截取的字符
   return R

# 正则清除
def clear(html,regexs):
   if regexs == '' : return html
   for regex in regexs.split(chr(10)):
       regex = regex.strip()
       if regex != '' :
           if regex[:1]==chr(40) and regex[-1:]==chr(41):
               html = re.sub(regex,'',html,re.I|re.S)
           else :
               html = html.replace(regex,'')
   return html

# 格式化为路径
def en2path(enStr):
   return re.sub('[\W]+','-',en2chr(enStr),re.I|re.U).strip('-')

# 替换实体为正常字符
def en2chr(enStr):
   return enStr.replace('&amp;','&')

# ------------------------------------- 开始执行程序 -------------------------------------------


# 开始采集
loops = 0
while True:
   if loops>0 :
       url = getOneUrl()
       if url == "" :
           loops = 0
       else :
           loops = collect(url)
   else :
       loops = collect()
   # 暂停
   time.sleep(sleep)
   if loops==0 : break
       
# 关闭HTTP连接
dl.close()
# 退出程序 
sys.exit()
