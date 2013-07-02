# coding=gbk
import os,sys

#定义全局变量；c文件检查数量
filenum = 0

#trace检查函数
def check_trace(c_file,log):
  entry_num = 0
	exit_num = 0
	src_file = open(c_file,'r')
	#读取文件每一行，查找entry和exit
	for line_buf in src_file:
		if line_buf.find("ASON_TRC_ENTRY(") >= 0 :
			entry_num = entry_num + 1
		elif line_buf.find("ASON_TRC_EXIT(") >= 0 :
			exit_num = exit_num + 1
	if entry_num != exit_num :
		log.write(c_file + '  '+ str(entry_num) + '  '+ str(exit_num) + '\n')
	src_file.close()
	
#遍历当前目录
def listdir(dir,file):
	list = os.listdir(dir)
	for line in list:
		filepath = os.path.join(dir,line)
		#跳过.svn目录
		if line == '.svn' :
			continue;
		#递归当前文件夹
		if os.path.isdir(filepath) :
			listdir(filepath,file)
		elif os.path:
			#检查.c文件
			if line[-1]=='c' and line[-2] == '.' :
				print line
				check_trace(filepath,file)
				global filenum
				filenum += 1

def main():   
        #dir = "D:\svn\svn\ZXUCP_A200_V1.20"
        dir = os.getcwd()
        myfile = open('trace_check.log','w')
        myfile.write('文件名' + '  '+ 'entry_num' + '  '+ 'exit_num' + '\n')
        listdir(dir,myfile)
        myfile.write(str(filenum) + '  file check' + '\n')
        myfile.close()
if __name__ == '__main__':
        main()
