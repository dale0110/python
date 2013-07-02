#encoding=gbk
# svnDateLineCount.py
#     Calculate numbers of lines each day committed
# in a svn repository.
#  some code come from http://tctianchi.yo2.cn/
########################################
# CONFIG
########################################
svnLogCommandhead = r'svn log %(dir)s'
svnLogCommandtail = r' -r %(data1)s:%(data2)s --diff'
svnLogCommand = r'svn log %(dir)s -r %(data1)s:%(data2)s'
exts = ['.c', '.h']

svnBlameCommand = r'svn blame -x -w %s'

svnUpdateCommand = r'svn update %s'

svnlogtxt = open("svnlog.txt",'w')
svnretxt  = open("svnres.txt",'w')
#fresult = open("")
totaladd = 0
totalmin = 0
########################################
# GLOBLAL
########################################
import os
import re
import sys
import threading
import time
import string
import datetime

fileList=[]
versionList=[]
fileChangeMap = {}
root = ''
AuthorChangeMap = {}

class svnLogCheck(threading.Thread):

    mypath = ''
    mycmd = ''
    #初始化
    def __init__(self, lock, threadName, version1, path1):
        super(svnLogCheck, self).__init__(name = threadName)
        self.lock = lock
        self.mypath = path1
        global svnLogCommand
        #self.mycmd = svnLogCommandhead %{'dir' : self.mypath}
        #self.mycmd = self.mycmd + svnLogCommandtail
        #print version1
        self.mycmd = svnLogCommand % {'dir':path1, 'data1':version1, 'data2':version1} + ' --diff'
        #print self.mycmd
    #run    
    def run(self):
        from os import popen
        #文件起始位置
        start=re.compile(r'---[ \t]')
        comin=re.compile(r'-[^-]+')
        coplus=re.compile(r'\+[^\+]+')
        startAu = re.compile(r'r[1-9]+[0-9]*[ \t]+\|[ \t]+[a-zA-Z0-9]+[ \t]+\|[ \t]+[1-2]+[0-9]+')
        
        vflg = 0
       # filename = ((self.mypath).split('\\'))[len((self.mypath).split('\\')) - 1].strip()
        newcmd = self.mycmd
        pipe = os.popen(newcmd)
        filename=''
        #读取所有输出
        res = pipe.readlines()
        self.lock.acquire()
        #初始化列表
        fileList=[]
        listtemp = []
        otherList=[]
        NowFileKey = ''
        NowAuKey = ''
        presentadd = 0
        presentmin = 0
        global totaladd
        global totalmin
        global AuthorChangeMap
        global fileChangeMap
        #逐条遍历
        for text in res:
            svnlogtxt.write(text+'\n')
            #去除换行符
            text = text[0:-1]
            #判断是否是起始行
            if(start.match(text)):
                str1=text.split()[1]
                str1=str1.split(r'/')[len(str1.split(r'/'))-1].strip()
                #文件类型判断
                if str1.endswith('.c') or str1.endswith('.h'):
                    NowFileKey = str1.strip()
                    filename = str1
                    listtemp.append(filename)
                else:
                    NowFileKey = ''
                    otherList.append(str1.strip())
                if vflg == 0:
                    versonStart = 0
                    versonEnd = 0
                    
            elif(startAu.match(text)):           
                au=text.split('|')[1].strip()
                NowAuKey = au
                if NowAuKey <> '':
                    if AuthorChangeMap.has_key(NowAuKey):
                        AuthorChangeMap[NowAuKey][0] += presentadd
                        AuthorChangeMap[NowAuKey][1] += presentmin
                    else:
                        AuthorChangeMap[NowAuKey] = [presentadd,presentmin,[]]
                    for ii in listtemp:
                        if ii not in AuthorChangeMap[NowAuKey][2]:
                            AuthorChangeMap[NowAuKey][2].append(ii)
                    presentadd = 0
                    presentmin = 0
                    listtemp = []
                    
            elif comin.match(text) or text == '-':
                if NowFileKey <> '':
                    totalmin +=1
                    presentmin += 1
                    if fileChangeMap.has_key(NowFileKey):
                        fileChangeMap[NowFileKey][1] += 1
                    else:
                        keyvalue=[0,1]
                        fileChangeMap[NowFileKey] = keyvalue
            elif coplus.match(text) or text == '+':
                if NowFileKey <> '' :
                    totaladd +=1
                    presentadd +=1
                    if fileChangeMap.has_key(NowFileKey):
                        fileChangeMap[NowFileKey][0] += 1
                    else:
                        keyvalue = [1,0]
                        fileChangeMap[NowFileKey] = keyvalue
                      
        self.lock.release()    
        pipe.close()
        
        
        
    
########################################
# SEARCH
########################################
from os.path import basename, isdir, join
from os import listdir
def walkIn(path, depth=0):
    #prefix = depth* '| ' + '-'
    if(isdir(path)):
        #print prefix, basename(path)
        for item in listdir(path):
            walkIn(os.path.join(path, item), depth + 1)
    else:
        #print prefix, basename(path)
        if os.path.splitext(path)[1] in exts:
            #print path
            fileList.append(path)

########################################
# SEARCH
########################################
def getAllVerson(dir1, date1, date2):
    print "get all versions between please wait ..."
    startAu = re.compile(r'r[1-9]+[0-9]*[ \t]+\|[ \t]+[a-zA-Z0-9]+[ \t]+\|[ \t]+[1-2]+[0-9]+')
    global svnLogCommand
    svnLogCommand1 = svnLogCommand % {'dir':dir1, 'data1':date1, 'data2':date2}
    pipe = os.popen(svnLogCommand1)
    res = pipe.readlines()
    for text in res:
        if startAu.match(text):
            numstr = text.split()[0]
            numstr = numstr.split('r')[1]
            versionList.append(numstr)
    
########################################
# 空格填充
########################################
def spaceRt(num):
    strx = ''
    i = 0
    while i < num:
        strx += ' '
        i+=1
    return strx
########################################
# total calc
########################################
def totalCalc():
    #print "startat: " + time.time() 
    myKeys = fileChangeMap.keys()
    myKeys.sort()
    svnlogtxt.write('------------------------------------------------------------------------------\n')
    for myKey in myKeys:
        svnlogtxt.write(str(myKey)+ spaceRt(12-len(str(myKey))) +  \
                        str(fileChangeMap[myKey][0]) + spaceRt(7-len(str(fileChangeMap[myKey][0]))) + \
                        str(fileChangeMap[myKey][1]) )      
        svnlogtxt.write('\n')
    myKeys = AuthorChangeMap.keys()
    myKeys.sort()
    svnretxt.write('--------------------------------svndatelinecount---------------------------------------\n')
    svnretxt.write('usrname:          add:      del:      files:\n')
    for verNum in myKeys:
        svnretxt.write(str(verNum)+ spaceRt(18 - len(str(verNum))) + \
                        str(AuthorChangeMap[verNum][0]) + spaceRt(10 - len(str(AuthorChangeMap[verNum][0]))) + \
                        str(AuthorChangeMap[verNum][1]) + spaceRt(10 - len(str(AuthorChangeMap[verNum][1]))) + '(')
        i = 0
        for ii in AuthorChangeMap[verNum][2]:
            i+=1
            if 6==i:
                svnretxt.write('\n'+spaceRt(38))
                i = 0
            if ii == AuthorChangeMap[verNum][2][len(AuthorChangeMap[verNum][2]) - 1] :                
                svnretxt.write(str(ii) + '')
                i = 0
            else:
                svnretxt.write(str(ii) + ',')
                
        svnretxt.write(')\n')
    global totaladd
    global totalmin
    svnretxt.write('----------------\n')
    svnretxt.write('totaladd: ' + str(totaladd) + '\n')
    svnretxt.write('totalmin: ' + str(totalmin) + '\n')

########################################
# MAIN
########################################
if __name__ == '__main__':
    
    print sys.argv.__len__()
    print sys.argv[0]
    from os.path import isdir
    maxThreadNums =101
    nowThreadNums =0
    if(sys.argv.__len__() >= 5):
        if(sys.argv[2] == 'd'):
            #svnLogCommandtail = svnLogCommandtail % {'data1':'{'+ str(sys.argv[3]) + '}', 'data2':'{' + str(sys.argv[4] + '}')}
            getAllVerson(root, '{'+ str(sys.argv[3]) + '}', '{' + str(sys.argv[4] + '}'))
        else:
            #svnLogCommandtail = svnLogCommandtail % {'data1':str(sys.argv[3]) , 'data2':str(sys.argv[4])}
            getAllVerson(root, str(sys.argv[3]), str(sys.argv[3]))
        root = sys.argv[1]
        if (sys.argv.__len__() == 6):
            maxThreadNums = string.atoi(sys.argv[5]) + 1
            print sys.argv[5]
    else:
        date1 = datetime.date.today()
        time1 = datetime.timedelta(1)
        date2 = date1 + time1
        print date1.__str__()
        #svnLogCommandtail = svnLogCommandtail % {'data1':'{'+ date1.__str__() + '}', 'data2':'{' + date2.__str__() + '}'}       
        root = '.'       
        getAllVerson(root, '{'+ date1.__str__() + '}', '{' + date2.__str__() + '}')
    
    #print svnLogCommandtail
    
    #walkIn(root)
    #totalFileNums = len(fileList) 
    #print '总共需要处理的文件数: ' + str(totalFileNums)
    #print '最大线程数:' + str(maxThreadNums - 1)
    #cd  = raw_input('请确认: ')
    lock = threading.Lock()
    i = 0
    vlength=str(len(versionList))
    for ii in versionList:
        nowThreadNums = threading.activeCount()
        while nowThreadNums >= maxThreadNums:
            time.sleep(15)
            nowThreadNums = threading.activeCount()
        svnLogCheck(lock, "thread-" + str(i), str(ii), root).start()
        print '进度: ' + str(i+1) +"/"+ vlength
        print '当前处理中: ' + str(threading.activeCount() -1)
        i +=1
    nowThreadNums = threading.activeCount()
    print '已经全部投入处理，等待处理完成 .'
    while nowThreadNums > 1:
        time.sleep(10)
        if not nowThreadNums == threading.activeCount():
            nowThreadNums = threading.activeCount()
            print '还在处理中的进程数量: ' + str(nowThreadNums - 1)
    totalCalc()
    svnlogtxt.close()
    svnretxt.close()
      
