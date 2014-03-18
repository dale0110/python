# -*- coding: utf-8 -*-

import re
import codecs
from PIL import Image,ImageFont,ImageDraw




'''计算中文汉字数量'''                          
def zh_count(string):
    re_zh = ur'[\u4e00-\u9fa5]'
    pattern = re.compile(re_zh)
    return len(pattern.findall(string))

'''计算中文汉字数量'''                          
def char_count(string):
    re_char = '[a-zA-Z][a-zA-Z0-9_.,;!?，。？；：]'
    pattern = re.compile(re_char)
    return len(pattern.findall(string))
                               

'''初始化全局变量'''
#字体大小
font_size=20

#每行文本高度
char_height=font_size*1
char_length=font_size*1

line_max=0
colum_max=0

#图片宽度
pic_length=0
#图片长度
pic_height=char_height


'''写一行文本'''
def draw_line(x,y,text,font):
    draw.text((x,y),text,(0,0,0),font)

def draw_line2(x,y,text,font):
    colum = 0
    while colum<colum_max :
        print "colum:%d"  %colum 
        draw.text((x+font_size*colum,y),unicode(text,'utf-8'),(0,0,0),font)
        colum+=1
    

def draw_text(txt_file,font):
    src_file = open(txt_file,'r')
    line=0
    for line_buf in src_file:
        #print line_buf.encode('utf-8')
        #print line_buf.decode('gbk') 
        draw_line(0,char_height*line,line_buf.decode('gbk'),font)
        line+=1
    src_file.close()

def get_max(txt_file):
    src_file = open(txt_file,'r')
    line=0
    for line_buf in src_file:
        txt=line_buf.decode('gbk')
        colum_length=zh_count(txt)+char_count(txt)
        global colum_max,line_max,pic_length,pic_height,char_length,char_height
        print "%d %d %d %d" %(line_max,colum_max,pic_length,pic_height)
        if colum_length>colum_max:
            colum_max=colum_length
        line+=1
    line_max=line
    #图片宽度
    pic_length=colum_max*char_length
    #图片长度
    pic_height=line_max*char_height
    src_file.close() 

#def main():
    
get_max("test.txt")
print "%f %f %f %f" %(line_max,colum_max,pic_length,pic_height)

'''图片基本信息'''
font = ImageFont.truetype('simsun.ttc',font_size)
img = Image.new('RGB',(pic_length,pic_height),(255,255,255))
draw = ImageDraw.Draw(img)

'''
line = 0
while line<line_max :
    print "line:%d"  %line 
    #draw_line(0,line_height*line,"你好")
    #draw_line2(0,char_height*line,"你",font)
    line+=1
'''
draw_text("test.txt",font)

 
img.save('test.jpg','JPEG')
    
#if __name__ == "__main__":
#    main()
