# coding=utf-8

import os
import time
import sys
import thread
import string
import platform
import logging

ftplogger=0


def logger_init():
      
    ''' 创建一个logger ''' 
    logger = logging.getLogger('pinglogger')  
    logger.setLevel(logging.DEBUG)  
      
    ''' 创建一个handler，用于写入日志文件 '''
    fh = logging.FileHandler('ping.log')  
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


def isUp(hostname):
    global ftplogger
    
    giveFeedback = True

    if platform.system() == "Windows":
        response = os.system("ping "+hostname+" -n 4")
    else:
        response = os.system("ping -c 4 " + hostname)

    isUpBool = False
    if response == 0:
        if giveFeedback:
            print hostname, 'is up!'
            ftplogger.info(hostname+':UP')
        isUpBool = True
    else:
        if giveFeedback:
            print hostname, 'is down!'
            ftplogger.info(hostname+':DOWN')

    return isUpBool




#通过读取配置文件上载ftp文件
def main():
    global ftplogger
    ftplogger=logger_init()
    ftplogger.info("start ping test")
    try:
        configfile = open("config.ini",'r')
        while 1: 
            message=configfile.readline()
            if len(message)< 10:
                break
            list1=message.split()
            print "host="+list1[0]
            host=list1[0]
            if not ( host=="") :
                isUp(str(host))
            else :
                print "configfile error"
        configfile.close()
    except Exception,ex:
        print Exception,":",ex
        time.sleep(5)
    ftplogger.info("test end")
    return 0

#-------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
