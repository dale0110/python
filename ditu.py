# -*- coding=utf-8 -*- 
import json
from selenium import webdriver
#打开浏览器
browser = webdriver.Chrome()
#urls = 'https://ditu.amap.com/service/regeo?longitude=114.447376&latitude=30.526071' #自行由上面步骤获取
urls = 'https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=13&city=420100&geoobj=114.45904%7C30.469083%7C114.568902%7C30.585749&_src=around&keywords=%E7%BE%8E%E9%A3%9F' #自行由上面步骤获取
#urls = 'https://ditu.amap.com/service/regeo?longitude=114.455399&latitude=30.532226' #自行由上面步骤获取炸鸡

browser.get(urls)
html_source = browser.page_source

#print html_source

#推出浏览器
browser.quit()
#因拉的源码前后有html文本，截取字符串即可
d = json.dumps(html_source[84:-20],ensure_ascii=False)
d1 = json.loads(d)
print d1

#转为字典
d2 = eval(d1)
for i in range(len(d2['data']['poi_list'])):
    #打印商户名称、地址、联系方式
    print([d2['data']['poi_list'][i]['name'],d2['data']['poi_list'][i]['address'],d2['data']['poi_list'][i]['tel']])
    break

