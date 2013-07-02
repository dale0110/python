# coding=gbk
#############################################################################################
#函数名：ftpLogDownLoad
#描  述：保存wason log信息 
#参  数：
#       host 服务器ip
#       port 端口号
#返  回：
#作  者：倪敬宾
#修改说明：无
#创建日期 2012-3-13
#############################################################################################

import ftplib
import os
import telnetlib
import time
import sys
import thread
import string
#下载文本文件
#----------------------------------------------------------------------------------------------
def gettext(ftp, filename, outfile=None):
    if outfile is None:
        outfile = sys.stdout
    # use a lambda to add newlines to the lines read from the server
    ftp.retrlines("RETR " + filename, lambda s, w=outfile.write: w(s+"\n"))
    
#下载二进制文件
#----------------------------------------------------------------------------------------------
def getbinary(ftp, filename, outfile=None):
    if outfile is None:
        outfile = sys.stdout
    ftp.retrbinary("RETR " + filename, outfile.write)
    
#根据文件类型下载多个文件
#----------------------------------------------------------------------------------------------
def getFilesByType(ftp,fileType,wkdir,saveAt):
    if saveAt=="" :
        dirSave = os.getcwd()
    else:
        dirSave=saveAt
    ftp.cwd("/")
    ftp.cwd(wkdir)
    list1=ftp.nlst(".")
    for ii in list1:
        if ii.endswith(fileType):
            dirSave1=dirSave+"\\"+ii
            print dirSave1
            outfile = open(dirSave1,'w')
            #cmd = "SIZE "+ii
            #ret = ftp.sendcmd(cmd)
            #fileSize=ret.split()[1]
            #print fileSize
            #fileSizeN=string.atoi(fileSize)
            #print ii+" size ="+fileSizeN+" kb start download."
            sys.stdout.flush
            getbinary(ftp,ii,outfile)
            outfile.close()
            dirSave1=dirSave
            print ii+" have downloaded."
    return 0

#保存节点telnet信息到文件
#----------------------------------------------------------------------------------------------
def telnetInfoSave(cmdList,hostIp,port=23,dirS=""):
    HOST = hostIp
    USER = "zte"
    PASSWORD = "zte"
    try:
        telnet = telnetlib.Telnet(HOST,port)
        time.sleep(0.5)
        telnet.write(USER + "\r")
        time.sleep(0.5)
        telnet.write(PASSWORD + "\r")
        time.sleep(0.5)
        telnet.write("show\n\r")
        time.sleep(0.5)
        telnet.write(":time\r")
        time.sleep(0.5)
        telnet.write("sh 2\n\r")
        time.sleep(0.5)
        telnet.write("\n\r")
        time.sleep(0.5)
        telnet.write("main-cmd showcpsysstat\r")
        time.sleep(0.5)

        telnet.write("\n\r")
        time.sleep(0.5)
        count =1
        str1=""
        for ii in cmdList :
            telnet.write("\r")
            time.sleep(0.5)
            telnet.write( ii+"\r")
            time.sleep(0.5)
            str1=str1+telnet.read_very_eager()
        telnet.write("exit\n\r")
        telnet.close()
    except Exception ,e:
        print Exception,':',e
        time.sleep(5)
        print "telnet失败！\n"
        return -1
    #-----------------------------------
    if dirS=="":
        dir1 = os.getcwd()
    else:
        dir1=dirS
    now=time.localtime(time.time())
    now=time.strftime("%Y/%m/%d %H:%M", now)
    name=hostIp
    try:
        myfile = open(dir1+'\\'+name+'\\'+name+'cmdInfo.log','w')
        print dir1+'\\'+name+'\\'+name+'cmdInfo.log'
        myfile.write(now+"\n")
        myfile.write(str1+"\n")
        myfile.close()
    except Exception,ex:
        print Exception,':',ex
        time.sleep(5)
    print HOST + " information save completed\n"
    #-----------------------------------
    return 0

#删除指定目录下所有文件
#----------------------------------------------------------------------------------------------
def removeAll(wkdir):
    if wkdir=="":
        wkdir=os.getcwd()
    list1=os.listdir(wkdir)
    for ii in list1:
        os.remove(wkdir+"\\"+ii)
    return 0

#下载ftp上log文件
#----------------------------------------------------------------------------------------------
def ftpLogDownLoad (host,user,passwd,cmdList,port=23,dirS=""):
    USER = user
    PASSWORD = passwd
    print user+":"+passwd+"\n"
    flag=0
    try:
        telnet = telnetlib.Telnet(host,23)
        time.sleep(0.5)
        telnet.write("/home/sysdata/app/zftpd -p 9000 \r")
        time.sleep(0.5)
        telnet.close()
        time.sleep(1)
    except Exception,ex:
        print Exception,":",ex
        flag=1
        
    derect=os.getcwd()
    
    if not dirS=="":
        derect=derect+"\\"+dirS
        if not os.path.exists(derect):
            os.mkdir(derect)
          
    derectHost=derect+"\\"+host
    if not len(cmdList)==0 :
        try:
            thread.start_new(telnetInfoSave,(cmdList,host,port,dirS,))
        except Exception,ex:
            print Exception,":",ex
        
    derect1=derectHost+"\\sd"
    derect2=derectHost+"\\log"
    if not os.path.exists(derectHost):
        os.mkdir(derectHost)
    if not os.path.exists(derect1):
        os.mkdir(derect1)
    if not os.path.exists(derect2):
        os.mkdir(derect2)
    removeAll(derect1)
    removeAll(derect2)

    if flag==1:
        telnetError = open(derectHost+"\\telnetError.log",'w')
        telnetError.write("telnet失败\n")
        telnetError.close()
    try:
        ftp = ftplib.FTP(host)
        ftp.login(USER,PASSWORD)
        getFilesByType(ftp,".log",".",derect2)
        getFilesByType(ftp,".bak",".",derect2)
        getFilesByType(ftp,".log","home/sd/wason",derect1)
        getFilesByType(ftp,".bak","home/sd/wason",derect1)
        ftp.quit()
    except Exception,ex:
        print Exception,":",ex
        FtpError = open(derectHost+"\\FtpError.log",'w')
        for ii in ex:
            FtpError.write(ii+"\n")
        FtpError.close()
    return 0

#通过读取配置文件下载ftp上log
def downLogByConfile():
    try:
        configfile = open("config.ini",'r')
        cmdListFile = open("cmdList.txt",'r')
        cmdList=[]
        message=cmdListFile.readline()
        while not message=="":
            cmdList.append(message)
            message=cmdListFile.readline()
        now=time.localtime(time.time())
        now=time.strftime("%Y_%m_%d_%H_%M_%S", now)
        while 1: 
            message=configfile.readline()
            if len(message)< 10:
                break
            list1=message.split()
            print "host="+list1[0]+" port="+list1[1]
            host=list1[0]
            port=list1[1]
            user=list1[2]
            passwd=list1[3]
            if not ( host=="" or port=="") :
                #try:
                    #thread.start_new(ftpLogDownLoad,(str(host),str(user),str(passwd),str(port),str(now),))
                    #time.sleep(5)
                #except Exception,ex:
                    #print Exception,":",ex    
                ftpLogDownLoad(str(host),str(user),str(passwd),cmdList,str(port),str(now))
            else :
                print "configfile error"
        configfile.close()
        cmdListFile.close()
    except Exception,ex:
        print Exception,":",ex
        time.sleep(5)
    return 0

#-------------------------------------------------------------------------------
downLogByConfile()
