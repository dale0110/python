# -*- coding: utf-8 -*-

import re
from PIL import Image,ImageFont,ImageDraw


def check_name_format(name):
    re_name = ur'^([a-zA-Z][\w]{2,19}|[\u4e00-\u9fa5]{1,10}|[\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5\w]{2,19})$'
    pattern = re.compile(re_name)
    match = pattern.match(name)
    if match:
        return True if len(name) + zh_count(name) <= 20 else False
    else:
        return False

                          
def zh_count(string):
    re_zh = ur'[\u4e00-\u9fa5]'
    pattern = re.compile(re_zh)
    return len(pattern.findall(string))
                               

'''初始化全局变量'''
#字体大小
font_size=20
#图片宽度
pic_length=800
#图片长度
pic_height=1024
#每行文本高度
char_height=font_size*1.2
char_length=font_size*1

line_max=pic_height/char_height
colum_max=pic_length/char_length

'''写一行文本'''
def draw_line(x,y,text,font):
    draw.text((x,y),unicode(text,'utf-8'),(0,0,0),font)

def draw_line2(x,y,text,font):
    colum = 0
    while colum<colum_max :
        print "colum:%d"  %colum 
        draw.text((x+font_size*colum,y),unicode(text,'utf-8'),(0,0,0),font)
        colum+=1
    

def get_text(txt_file):
    src_file = open(txt_file,'r')
    for line_buf in src_file:
        if line_buf.find("ASON_TRC_ENTRY(") >= 0 :
            pass
        elif line_buf.find("ASON_TRC_EXIT(") >= 0 :
            pass
    src_file.close() 

'''图片基本信息'''
font = ImageFont.truetype('simsun.ttc',font_size)
img = Image.new('RGB',(pic_length,pic_height),(255,255,255))
draw = ImageDraw.Draw(img)



line = 0
while line<line_max :
    print "line:%d"  %line 
    #draw_line(0,line_height*line,'''你好''')
    draw_line2(0,char_height*line,'''你''',font)
    line+=1


 
img.save('test.jpg','JPEG')
