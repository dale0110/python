#encoding=gbk
import sys
import os
import re
#kide结果解析
pathNow=os.getcwd()
#--------------------------------------------------
def getEachMatchLineCount(fileName,mname):
    myfile = open(pathNow+'\\lint_errorlog.txt','a')
    keword1='Warning'
    keword2='Error'
    keword3='Info'
    lintLog=open(fileName,'r')
    line=lintLog.readline()
    i=0;
    print mname
    mname=re.compile(mname)
    keword1=re.compile(keword1)
    keword2=re.compile(keword2)
    keword3=re.compile(keword3)
    j=0;
    err=0;
    war=0;
    info=0;
    while(line):
        if mname.search(line) >= 0 :
            if keword1.search(line) >=0 : 
                war=war+1
                myfile.write(line+'\n')
            elif keword2.search(line) >=0 :
                err=err+1
                myfile.write(line+'\n')
            elif keword3.search(line) >=0 :
                info=info+1
        line=lintLog.readline()
        j=j+1;
    listR=[err,war,info]
    myfile.close()
    return listR;
#--------------------------------------------------
def getAllMatchLineCount():
    myfile = open(pathNow+'\\lintResult.txt','w')
    listMu=['app\\\\aep','app\\\\aps','app\\\\coms','app\\\\da','app\\\\db','app\\\\if','app\\\\init',\
            'app\\\\lrm','app\\\\main','app\\\\nbase','pce\\\\alg','pce\\\\pic','pce\\\\pub','pce\\\\rpc',\
            'pce\\\\rrm','app\\\\pub','app\\\\sc','app\\\\ssm','app\\\\ta\\\\','app\\\\tap\\\\']
    #lintLogM=open(pathNow+'\\record\\'+fileName,'r')
    myfile.write('module:\t\t error:\t\t warinng:\t\t info:\n')
    for ii in listMu:
      
      data = getEachMatchLineCount(pathNow+'\\Lint_A.log',ii)
      if not ii.split('\\\\')[0] == 'pce' :
          myfile.write(ii.split('\\\\')[1]+'\t\t    '+str(data[0])+'\t\t    ' \
                       +str(data[1])+'\t\t\t '+str(data[2])+' \n')
      else:
          myfile.write('pce:'+ii.split('\\\\')[1]+'\t\t    '+str(data[0])+'\t\t    ' \
                       +str(data[1])+'\t\t\t '+str(data[2])+' \n')
    myfile.close() 
    return 0;
#--------------------------------------------------
myfile = open(pathNow+'\\lint_errorlog.txt','w')
myfile.close();
getAllMatchLineCount()
