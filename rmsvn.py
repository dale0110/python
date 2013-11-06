# coding:utf8
import os,sys
        
#遍历当前目录
def listdir(dir):
    list = os.listdir(dir)
    for line in list:
        filepath = os.path.join(dir,line)
        #跳过.svn目录
        if line == '.svn' :
            os.rmdir(".svn")
        #递归当前文件夹
        if os.path.isdir(filepath) :
            listdir(filepath)
        elif os.path:
            continue

def main():   
        dir = os.getcwd()
        listdir(dir)
if __name__ == '__main__':
        main()
