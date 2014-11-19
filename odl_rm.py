# coding:utf8
import os,sys

dire_depth=0


#重命名当前目录下文件名字
def dir_rename(dir):
    dir_num=0
    list = os.listdir(dir)
    os.chdir(dir)
    for line in list:
        filepath = os.path.join(dir,line)

        #递归当前文件夹
        if os.path.isdir(filepath) :
            dir_num+=1
            print dir_num
            print os.renames(line,str(dir_num))
        else:
            print line
        
#遍历当前目录,删除文件
def loop_rmfile(dir):
    list = os.listdir(dir)
    os.chdir(dir)
    for line in list:
        
        filepath = os.path.join(dir,line)
        #递归当前文件夹
        if os.path.isdir(filepath) :
            loop_rmfile(filepath)
            os.chdir(dir)
            os.rmdir(line)
        else:
            print line
            try:
                os.remove(line)
            except os.error:
                pass
            finally:
                pass
            

#遍历当前目录,删除文件
def loop_rename(dir):
    dir_rename(dir)
    global dire_depth
    dire_depth+=1
    list = os.listdir(dir)
    os.chdir(dir)
    for line in list:
        filepath = os.path.join(dir,line)

        #递归当前文件夹
        if os.path.isdir(filepath) :
            print dire_depth
            os.chdir(dir)
            loop_rename(filepath)
            dire_depth-=1
        else:
            print line
            #os.remove(line)



def main():   
        dir = os.getcwd()
        loop_rename(dir)
        loop_rmfile(dir)
if __name__ == '__main__':
        main()
