# coding:utf-8
  
import csv
import os
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

    reader = csv.reader(open(file_name,'rU'), delimiter=",")
       
    for values in reader:
        #print ', '.join(values).decode('utf-8')
        if '|'.join(values).decode('utf-8').find("阳谷")>0:
            print ', '.join(values).decode('utf-8')
            
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
        
def find_in_csv(file_name):

    cvsfile=open(file_name,'rU')
    reader = csv.reader(cvsfile, delimiter=",")
    for values in reader:
        if ', '.join(values).decode('utf-8').find(key)>0:
            #print values
            #print ', '.join(values).decode('utf-8')
            global csvwriter
            csvwriter.writerow(', '.join(values).decode('utf-8'))
    cvsfile.close()

'''
    lineno = 0 

    try:

    except:
        print "Problem at line #",lineno
        print repr(values)
'''
            
def readdir(dir):
    #dir = os.getcwd()
    list = os.listdir(dir)
    for line in list:
        filepath = os.path.join(dir,line)
        if line.find(".csv"):
            #print line
            find_in_csv(filepath)




key="海淀"
def init_write():
    fd=open('test.csv', 'wb')
    csvwriter = csv.writer(fd,dialect='excel')
    return csvwriter
if __name__=="__main__":
    logger=logger_init()
    logger.info('start')
    csvwriter=init_write()
    #read_csv("5000.csv")
    readdir("E:/python/src/2000W")
    #find_in_csv('阳谷',"5000.csv"）
    logger.info('end')
