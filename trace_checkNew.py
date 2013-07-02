#encoding=gbk
import sys
import os
import re
#获取当前目录 
pathNow=os.getcwd()
#log文件声明
myLog = open(pathNow+'\checkTotal.log','w')
myErrorLog = open(pathNow+'\checkError.log','w')
fileLog = open(pathNow+'\checkfileLog.log','w')
#函数类
class FuncObj:
    #方法名
    funcName =''
    #是否在.c文件中声明
    isDeclare = 0
    #开始行
    startLine = 0
    #代码行数
    totalLines = 0
    #注释行数
    explLines = 0
    #注释是否违反规则
    expBrekRule = 0
    #空行行数
    empLines = 0
    #trace_entry数量
    entryNums = 0
    #trace_exit数量
    exitNums = 0
    #trace_flow数量
    flowNums = 0
    #trace_abnormal
    abnormalNums = 0
    #trace_error数量
    errorNums = 0
    #trace_detail数量
    detailNums = 0
    #totalTrace 数量
    totalTraceNums = 0
    #人口是否正确
    isEntryRight = 1
    #初始化函数
    def __init__(self):
        funcName = ''
        startLine = 0
        totalLines = 0
        explLines = 0
        entryNums = 0
        exitNums = 0
        flowNums = 0
        abnormalNums = 0
        errorNums = 0
        detailNums = 0
        empLines = 0
        isEntryRight = 1
        
    #打印方法信息    
    def printFuncDetail(self,outPutFile):
        print '--------------------------------------'
        print 'FunctionName   : ' + str(self.funcName)
        print 'totalLines     : ' + str(self.totalLines)
        print 'explLines      : ' + str(self.explLines)
        print 'entryNums      : ' + str(self.entryNums)
        print 'exitNums       : ' + str(self.exitNums)
        print 'flowNums       : ' + str(self.flowNums)
        print 'abnormalNums   : ' + str(self.abnormalNums)
        print 'errorNums      : ' + str(self.errorNums)
        print 'detailNums     : ' + str(self.detailNums)
        print 'totalTraceNums : ' + str(self.totalTraceNums)
        print 'empLines       : ' + str(self.empLines)
        return 0
    
    #返回方法信息
    def getFuncDetail(self):
        namesp = 65
        normalsp = 16
        strReturn = ''
        list1=[str(self.totalLines),str(self.explLines),str(self.empLines),str(self.entryNums), \
               str(self.exitNums),str(self.totalTraceNums),str(self.startLine)]
        if self.isEntryRight == 0:
            list1[3] += '(funcNameErr)'
        if self.expBrekRule ==1:
            list1[1] += '(BrekRule)'
        strReturn += str(self.funcName)
        if self.isDeclare ==2:
            strReturn +='(errdecl)'
        spneed = namesp -len(strReturn)
        while spneed > 0:
            strReturn += ' '
            spneed -= 1
        for ii in list1:
            spneed = normalsp - len(ii)
            strReturn += ii
            while spneed > 0:
                strReturn += ' '
                spneed -= 1
        
        return strReturn
    
    def isComform(self):
        #or self.totalTraceNums -2 <= 0
        #判断是否有问题
        if self.entryNums <> 1 or self.exitNums <> 1  or self.isEntryRight <> 1 or self.expBrekRule == 1 or self.isDeclare == 2:
            return -1
        else:
            return 0
    
#文件类
class FileObj:
    #文件名
    fileName = ''
    #代码行数
    totalLines = 0
    #注释行数
    explLines = 0
    #空行行数
    empLines = 0
    #函数列表
    funcList = []
    #函数数量
    funcNums = 0
    #ErrorFuncs
    listErrorFunc = []
    #是否需要输出error
    haveError = 0
    #错误的声明
    errordeclares = []
    #初始化函数
    def __init__(self):
        fileName = ''
        totalLines = 0
        explLines = 0
        funcList = []
        empLines = 0
        funcNums = 0
        listErrorFunc = []
    #打印文件信息    
    def printFileDetail(self,outPutFile) :
        print '----------------------------------------'
        print '文件: ' + str(selffileName)
        print '总行数: ' + str(self.totalLines)
        print '空行数: ' + str(self.empLines)
        print '注释行数: ' + str(self.explLines)
        print '方法数: ' + str(self.funcNums)
        return 0
    #返回文件信息
    def getFileDetail(self) :
        #print '----------------------------------------'
        'filename: totalLines: emptyLines: commentlines: functionNums:'
        namesp = 41
        normalsp = 16
        list1=[str(self.totalLines),str(self.explLines),str(self.empLines),str(self.funcNums)]
        strReturn = ''
        strName = self.fileName
        strNameList = strName.split('\\')
        strName =strNameList[len(strNameList) - 1]
        strReturn += str(strName)
        spneed = namesp -len(strReturn)
        while spneed > 0:
            strReturn += ' '
            spneed -= 1
        for ii in list1:
            spneed = normalsp - len(ii)
            strReturn += ii
            while spneed > 0:
                strReturn += ' '
                spneed -= 1
        
        return strReturn
        return 0
    #打印文件内所有方法信息
    def writeAllFuncMessage(self,logfile):
        headLine = 'functionName:                                                    '
        headLine += 'totalLines:     '
        headLine += 'commentLines:   '
        headLine += 'empLines:       '
        headLine += 'entryNums:      '
        headLine += 'exitNums:       '
        headLine += 'totalTraceNums: '
        
        headLine1 = ''
        i = 166
        while i>0:
           headLine1 = headLine1 + '-'
           i -= 1
        logfile.write(headLine1+ '\n')
        logfile.write('file: ' + self.fileName + '\n')
        logfile.write(headLine1 + '\n')
        logfile.write(headLine + '\n')
        logfile.write(headLine1 + '\n')
        for ii in self.funcList:
            logfile.write(ii.getFuncDetail() + '\n')
        return 0
    #打印文件内错误方法信息
    def writeErrorFuncMessage(self,logfile):
        if self.haveError <= 0:
            return 0
        headLine = 'functionName:                                                    '
        headLine += 'totalLines:     '
        headLine += 'commentLines:   '
        headLine += 'empLines:       '
        headLine += 'entryNums:      '
        headLine += 'exitNums:       '
        headLine += 'totalTraceNums: '
        
        headLine1 = ''
        i = 166
        while i>0:
           headLine1 = headLine1 + '-'
           i -= 1
        '''
        print headLine1
        print 'file: ' + self.fileName
        print headLine1
        print headLine
        print headLine1
        for ii in self.listErrorFunc:
            print ii.getFuncDetail()
        '''
        logfile.write(headLine1 + '\n')
        logfile.write('file: ' + self.fileName + '\n')
        logfile.write(headLine1 + '\n')
        logfile.write(headLine + '\n')
        logfile.write(headLine1 + '\n')
        for ii in self.listErrorFunc:
            logfile.write(ii.getFuncDetail() + '\n')
        return 0
#收集方法信息
#-------------------------------------------------
def getEachFuncDetail(fd,funcName,startLine,line):
    flagNoUsed = 0
    #'{'匹配对象
    funcStart = re.compile(r'[ \t]*[{{]')
    #'}'匹配对象
    funcEnd = re.compile(r'[ \t]*[}}]')
    #非空行匹配
    notEmptLine = re.compile(r'[ \t]*\S')
    # #if 0匹配
    ifZeroBegin = re.compile(r'[ \t]*#if[ \t]*0')
    # #endif 匹配
    endifLine = re.compile(r'[ \t]*#endif')
    # ;匹配
    lineEnd = re.compile(r';')
    #trace信息
    entry = re.compile(r'[ \t]*ASON_TRC_ENTRY')
    error = re.compile(r'[ \t]*ASON_TRC_ERROR')
    detail = re.compile(r'[ \t]*ASON_TRC_DETAIL')
    abnorm = re.compile(r'[ \t]*ASON_TRC_ABNORM')
    flow = re.compile(r'[ \t]*ASON_TRC_FLOW')
    fexit = re.compile(r'[ \t]*ASON_TRC_EXIT')
    #注释匹配对象
    zhushi = re.compile(r'[ \t]*/\*')
    #注释尾匹配对象
    zhushiend = re.compile('\*/')
    #方法对象实例
    funcNow = FuncObj()
    funcNow.funcName = funcName
    #左括号剩余数量
    inLefCount = 0
    #方法行数
    count = 0
    funcNow.startLine = startLine
    #查找方法开始'{'
    while(line):
        if len(lineEnd.findall(line))>0:
            funcNow.isDeclare = 1
            return [fd,startLine,funcNow] 
        if funcStart.match(line) >= 0:
            inLefCount =  1
            break
        line = fd.readline()
        startLine = startLine + 1
        
    line = fd.readline()
    #遍历方法每一行
    while(line):
        #过滤掉#if 0注释掉的语句
        if ifZeroBegin.match(line) :
            count=count+1
            line=fd.readline()
            while not endifLine.match(line):
                count=count+1
                line=fd.readline()
        else:
            count=count+1
        startLine = startLine + 1
        #'{'匹配
        if funcStart.match(line) :
            inLefCount = inLefCount + len(funcStart.findall(line)) - len(funcEnd.findall(line))
        #trace匹配
        elif entry.match(line) :
            funcNow.entryNums = funcNow.entryNums + 1
            strStart = line.split('\"')[1]
            if strStart <> funcNow.funcName:
                funcNow.isEntryRight = 0
                print strStart + '!=' + funcNow.funcName + '|'
        #trace匹配
        elif error.match(line) :
            funcNow.errorNums = funcNow.errorNums + 1
        #trace匹配
        elif detail.match(line) :
            funcNow.detailNums = funcNow.detailNums + 1
        #trace匹配
        elif abnorm.match(line) :
            funcNow.abnormalNums = funcNow.abnormalNums + 1
        #trace匹配
        elif flow.match(line) :
            funcNow.flowNums = funcNow.flowNums + 1
        #trace匹配
        elif fexit.match(line) :
            funcNow.exitNums = funcNow.exitNums + 1
        #注释匹配
        elif zhushi.match(line) :
            if len(zhushiend.findall(line)) > 0:
                funcNow.explLines = funcNow.explLines + 1
            else:
                funcNow.expBrekRule = 1
                while(line):
                    funcNow.explLines = funcNow.explLines + 1
                    if len(zhushiend.findall(line)) > 0:
                        break
                    line = fd.readline()
                    count=count+1
        #空行匹配
        elif not notEmptLine.match(line) :
            funcNow.empLines = funcNow.empLines + 1
        #'}'匹配
        elif funcEnd.match(line) :
            inLefCount = inLefCount - 1
            if inLefCount == 0 :
               break
        line = fd.readline()
    #赋值
    funcNow.totalLines = count
    funcNow.totalTraceNums = funcNow.entryNums + funcNow.errorNums + funcNow.detailNums \
                             + funcNow.abnormalNums + funcNow.flowNums + funcNow.exitNums
    #funcNow.printFuncDetail(myLog)
    #print funcNow.getFuncDetail()
    return [fd,startLine,funcNow]

#收集文件信息
#--------------------------------------------------
def getEachFile(fileName):
    myfile=open(fileName,'r')
    line=myfile.readline()
    fileNow = FileObj()
    #列表初始化
    fileNow.funcList = []
    fileNow.listErrorFunc = []
    fileNow.errordeclares = []
    fileNow.fileName = fileName
    i=0
    #是否在方法体内
    inFucFlag = 0
    #方法头匹配对象
    lineBegin=re.compile('[a-zA-Z_]+[0-9]*[\*]*[ \t]*[\*]*[ \t]+[a-zA-Z_]+[((]')
    #注释匹配对象
    zhushi=re.compile(r'[ \t]*/\*')
    zhushi1=re.compile(r'[ \t]*\\\\')
    #空行匹配
    notEmptLine = re.compile(r'[ \t]*\S')
    # #if 0匹配
    ifZeroBegin = re.compile(r'[ \t]*#if[ \t]*0')
    # #endif 匹配
    endifLine = re.compile(r'[ \t]*#endif')
    #行数
    count=0
    #'{'未匹配数量
    inLefCount = 0
    #当前函数名称 
    funcName = ''
    while(line):
        #过滤掉#if 0注释掉的语句
        if ifZeroBegin.match(line) :
            count=count+1
            line=myfile.readline()
            while not endifLine.match(line):
                count=count+1
                line=myfile.readline()
        else:
            count=count+1
        #找到方法头查找匹配方法体
        if inFucFlag == 1:
            #调用方法处理函数
            list1 = getEachFuncDetail(myfile,funcName,count,line)
            count = list1[1]
            #print fileNow.fileName
            #print len(fileNow.funcList)
            if list1[2].isDeclare <> 1:
                if len(fileNow.errordeclares) > 0:
                    for ii in fileNow.errordeclares:
                        if ii.funcName == list1[2].funcName:
                            list1[2].isDeclare = 2
                            break
                fileNow.funcList.append(list1[2])
                fileNow.funcNums = fileNow.funcNums + 1
                fileNow.explLines = fileNow.explLines + list1[2].explLines
                fileNow.empLines = fileNow.empLines + list1[2].empLines
                if list1[2].isComform() == -1 :
                    fileNow.listErrorFunc.append(list1[2])
                    fileNow.haveError = fileNow.haveError + 1
            else:
                fileNow.errordeclares.append(list1[2])
            funcName =  ''
            inFucFlag = 0
        #查找方法头
        elif lineBegin.match(line)  :
            inFucFlag = 1
            funcName = line.split('(')[0]
            list1 = funcName.split()
            funcName = list1[len(list1)-1]
            #print str(count) +' '+ line
            #print funcName
        #注释
        elif zhushi.match(line) or zhushi1.match(line):
            fileNow.explLines = fileNow.explLines + 1
            #print str(count) +' '+ line
        #空行匹配
        elif not notEmptLine.match(line) :
            fileNow.empLines = fileNow.empLines + 1
        line=myfile.readline()
    fileNow.totalLines = count
    #fileNow.printFileDetail(myLog)
    #fileNow.writeAllFuncMessage(myLog)
    myfile.close()
    return fileNow
#遍历当前目录
#-----------------------------------------------
def getAllFile(dir1):
    list1 = os.listdir(dir1)
    listFile = []
    for line in list1:
        filepath = os.path.join(dir1,line)
  #跳过.svn目录
        if line == '.svn':
            continue
	#递归当前文件夹 
        if os.path.isdir(filepath):
            listR=getAllFile(filepath)
            for ii in listR:
                listFile.append(ii)	
        elif os.path:
	    #检查.c文件
            if line[-1]=='c' and line[-2] == '.' :
                listFile.append(getEachFile(filepath))
    return listFile

#--------------------------------------------------
def main():   
        dir1 = "E:\\code\\app"
        listFiles = []
        startLine = 'filename:                                '
        startLine += 'totalLines:     '
        startLine += 'emptyLines:     '
        startLine += 'commentlines:   '
        startLine += 'functionNums:   '
        startLine1 =''
        errorFuncNums = 0
        count = 105
        while count >0:
            startLine1 += '-'
            count -= 1
        fileLog.write(startLine1 + '\n')
        fileLog.write(startLine + '\n')
        fileLog.write(startLine1 + '\n')
        #dir1 = os.getcwd()
        listFiles = getAllFile(dir1)
        for ii in listFiles:
            #ii.printFileDetail(myLog)
            errorFuncNums += ii.haveError
            fileLog.write(ii.getFileDetail() + '\n')
            ii.writeErrorFuncMessage(myErrorLog)
            '''
            if len(ii.errordeclares) > 0:
                for j in ii.errordeclares:
                    print j.funcName
            '''
        print 'error fuc numbers = ' + str(errorFuncNums)    
            #print str(ii.fileName) + '  ' + str(ii.funcNums) + ' ' +str(len(ii.funcList))
                 
#---------------------------------------------------
myfile = open(pathNow+'\\codeCheck.log','w')
myfile.close()
#getEachFile(pathNow+'\\cc_agtsi_uni.c')
main()
#关闭log文件
myLog.close()
myErrorLog.close()
fileLog.close()
