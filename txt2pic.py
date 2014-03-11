# -*- coding: utf-8 -*-


 
from PIL import Image,ImageFont,ImageDraw


 
text = u'http://www.sharejs.com，test,hello'
 
 
font = ImageFont.truetype("simsun.ttc",24)
 
lines = []
line =''
 
 
for word in text.split():
    print word
    if font.getsize(line+word)[0] >= 300:
        lines.append(line)
        line = u''
        line += word 
        print 'size=',font.getsize(line+word)[0]
    else:
        line = line + word
 
 
 
line_height = font.getsize(text)[1]
img_height = line_height*(len(lines)+1)
 
 
print 'len=',len(lines)
print 'lines=',lines
 
im = Image.new("RGB",(444,img_height),(255,255,255))
dr = ImageDraw.Draw(im)
 
x,y=5,5
for line in lines:
    dr.text((x,y),line,font=font,fill="#000000")
    y += line_height
    
 
 
im.save("1.1.jpg")



'''
from PIL import Image,ImageFont,ImageDraw
font = ImageFont.truetype('simsun.ttc',24)
img = Image.new('RGB',(300,200),(255,255,255))
draw = ImageDraw.Draw(img)
draw.text( (0,50), u'你好,世界!',(0,0,0),font=font)
draw.text((0,90),unicode('你好','utf-8'),(0,0,0),font=font) 
img.save('test.jpg','JPEG')
'''




'''
import os
import StringIO
import Image,ImageFont,ImageDraw
import pygame
 
pygame.init()
 
text = u"这是一段测试文本，test 123。"
 
im = Image.new("RGB", (300, 50), (255, 255, 255))
#dr = ImageDraw.Draw(im)
#font = ImageFont.truetype(os.path.join("fonts", "simsun.ttc"), 18)

font = pygame.font.Font(os.path.join("fonts", "simsun.ttc"), 14)

#dr.text((10, 5), text, font=font, fill="#000000")
rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
 
#pygame.image.save(rtext, "t.gif")
#sio = StringIO.StringIO()
sio = "test4.jpg"
pygame.image.save(rtext, sio)
#sio.seek(0)
 
line = Image.open(sio)
im.paste(line, (10, 5))
 
im.show()
im.save("t.png")
'''
