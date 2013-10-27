# coding:utf-8
  
import csv

import logging  

def logger_init():
      
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
    return  logger


def read_csv(file_name):


    reader = csv.reader(open(file_name), delimiter=",")
   
    for values in reader:
        print  values
'''
    lineno = 0
    for values in reader:
        try:
            lineno += 1
            Name,ctfid,Gender,Address,Mobile,Version = values
        except:
            print "Problem at line #",lineno
            print repr(values)
            break
'''
'''
    for Name,ctfid,Gender,Address,Mobile,Version in reader:
        print Name,ctfid,Gender,Address,Mobile,Version
''' 
        
def find_in_csv(key,file_name):

    reader = csv.reader(open(file_name), delimiter=",")
     
    for Name,ctfid,Gender,Address,Mobile,Version in reader:
        if Address.find("阳谷") >= 0:
             print Name,ctfid,Gender,Address,Mobile,Version
        
if __name__=="__main__":
    logger=logger_init()
    logger.info('start')
    read_csv("5000.csv")
    #find_in_csv('阳谷',"5000.csv"）
    logger.info('end')
