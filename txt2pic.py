# -*- coding: utf-8 -*-

import re
import codecs
import chardet
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
font_size=24

#每行文本高度
char_height=int(font_size*1.2)
char_length=font_size*1

#图片宽度
pic_length=800
#图片长度
pic_height=0

line_max=0
colum_max=int(pic_length/char_length)


def draw_moreline(x,y,text,font,line):
    txt_code=chardet.detect(text)
    decode_text=text.decode(txt_code['encoding'])
    colum_length=len(decode_text)
    global colum_max,line_max,pic_length,pic_height,char_length,char_height
    print "txt_length:%d colum_length/colum_max:%d" %(len(decode_text),int(colum_length/colum_max))
    txt_num=int(colum_length/colum_max)+1
    print "txt_num:%d colum_length:%d" %(txt_num,colum_length)
    i=1
    print "colum_max:%d" %(colum_max)
    while i<=txt_num:
        print i
        if i<txt_num:
            line_buf=decode_text[(i-1)*colum_max:i*colum_max]
        elif i==txt_num:
            line_buf=decode_text[(i-1)*colum_max:colum_length]
        draw_oneline(x,char_height*line,line_buf,font)
        i+=1
        line+=1
    return line



'''写一行文本'''
def draw_oneline(x,y,text,font):
    print "x:%d y:%d" %(x,y)
    print text
    print len(text)
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
        line=draw_moreline(0,char_height*line,line_buf,font,line)
    src_file.close()

def get_max(txt_file):
    src_file = open(txt_file,'r')
    line=0
    for line_buf in src_file:
        #print line_buf
        if len(line_buf)==0:
            continue
        txt_code=chardet.detect(line_buf)
        txt=line_buf.decode(txt_code['encoding'])
        #print txt
        colum_length=len(txt)
        global colum_max,line_max,pic_length,pic_height,char_length,char_height
        line+=int(colum_length/colum_max)+1
    line_max=line
    #图片长度
    pic_height=line_max*char_height
    src_file.close()

#def main():
    
get_max("test.txt")
print "line_max:%f colum_max:%f pic_length:%f pic_height:%f" %(line_max,colum_max,pic_length,pic_height)

'''图片基本信息'''
font = ImageFont.truetype('simsun.ttc',font_size)
img = Image.new('RGB',(pic_length,pic_height),(255,255,255))
draw = ImageDraw.Draw(img)


draw_text("test.txt",font)

 
img.save('test.jpg','JPEG')
    
#if __name__ == "__main__":
#    main()
