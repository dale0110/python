# coding=utf-8

import ftplib
import os
import telnetlib
import time
import sys
import thread
import string

import logging

ftplogger=0

def logger_init():
      
    ''' 创建一个logger ''' 
    logger = logging.getLogger('ftplogger')  
    logger.setLevel(logging.DEBUG)  
      
    ''' 创建一个handler，用于写入日志文件 '''
    fh = logging.FileHandler('ftp.log')  
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
    return  logger


    

#上传二进制文件
#remotefile ：ftp存储该文件的路径+文件名
#filename：本地文件路径+文件名
#----------------------------------------------------------------------------------------------
    
def uploadfile(ftp,remotefile,filename):
    fp = open(filename,'rb')
    #print ftp.cwd(remotepath)
    ftplogger.info("from " +filename+" to "+remotefile)
    ftplogger.info(ftp.storbinary('STOR '+remotefile,fp,1024*4)) #上传文件    
    fp.close() #关闭文件  
   

#保存节点telnet信息到文件
#----------------------------------------------------------------------------------------------
def telnet_cmd(Ip,port=23):
    HOST = Ip
    USER = "zte"
    PASSWORD = "zte"
    try:
        telnet = telnetlib.Telnet(HOST,port)
        time.sleep(0.5)
        telnet.write(USER + "\r")
        time.sleep(0.5)
        telnet.write(PASSWORD + "\r")
        time.sleep(0.5)
        
        ftplogger.info("telnet OK")
            
        telnet.write("show\n\r")
        time.sleep(0.5)
        telnet.write(":time\r")
        time.sleep(0.5)
        #切换到WASON
        telnet.write("sh 5\n\r")
        time.sleep(0.5)
        telnet.write("\n\r")
        time.sleep(0.5)
        
        #telnet.write("main-cmd showcpsysstat\r")
        #time.sleep(0.5)

        telnet.write("\n\r")
        time.sleep(0.5)

        telnet.write(":sync \r")
        time.sleep(2)

        telnet.write(":reboot \r")
        time.sleep(0.5)
        '''
        count =1
        str1=""
        for ii in cmdList :
            telnet.write("\r")
            time.sleep(0.5)
            telnet.write( ii+"\r")
            time.sleep(0.5)
            str1=str1+telnet.read_very_eager()
        '''
        telnet.write("exit\n\r")
        telnet.close()
    except Exception ,e:
        print Exception,':',e
        time.sleep(5)
        ftplogger.error( "telnet error\n")
        return -1

    return 0


#ftp上载文件
#----------------------------------------------------------------------------------------------
def ftpupload(host,user,passwd):
    USER = user
    PASSWORD = passwd
    try:
        ftp = ftplib.FTP(host)
        ftp.login(USER,PASSWORD)
        ftp.set_debuglevel(0)
        uploadfile(ftp,'/home/sd/wason/nbase.ini','''F:\\test\\nbase.ini''')
        uploadfile(ftp,'/home/sd/SNP_WASON','''F:\\test\\SNP_WASON''')
        ftplogger.info('upload OK')
        ftp.quit()
    except Exception,ex:
        ftplogger.error(host+' error ')
    return 0

#通过读取配置文件上载ftp文件
def main():
    global ftplogger
    ftplogger=logger_init()
    try:
        configfile = open("config.ini",'r')
        cmdListFile = open("cmdList.txt",'r')
        cmdList=[]
        message=cmdListFile.readline()
        while not message=="":
            cmdList.append(message)
            message=cmdListFile.readline()
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
                ftplogger.info('start ftp:'+(str(host)))
                ftpupload(str(host),str(user),str(passwd))
                telnet_cmd(str(host),9023)
            else :
                print "configfile error"
        configfile.close()
        cmdListFile.close()
    except Exception,ex:
        print Exception,":",ex
        time.sleep(5)
    return 0

#-------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
