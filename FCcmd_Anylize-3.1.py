# coding:utf8
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MinuteLocator, SecondLocator
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
from StringIO import StringIO
import datetime as dt
import string
import sys


#    0                    1                        2                            3                                4                           5                      6                           7                           8                      9                    10                              10             11                          12 
#Num. | OriginFcId | RestoreFcId | trafficId |               StartTime        |         EndTime         |     RouteStartTime      |      RouteEndTime       |     CrossStartTime      |      CrossEndTime       |   Alarm Occured Time    | Restore Wait Time |  RestoreWaitStartTime   |   RestoreWaitEndTime
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### The example data
originStr = ""
if len(sys.argv) > 1 :
    # print sys.argv[1]
    f = open(sys.argv[1])
else:
    f = open("./traffic-restore-time.log")             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
while line:
    # print line,                 # 后面跟 ',' 将忽略换行符
    # print(line, end = '')　　　# 在 Python 3中使用
    originStr += line
    line = f.readline()

f.close()

a = StringIO(originStr)

#Converts str into a datetime object.
#str.lstrip() ： 去除字符串左边的空格
#str.rstrip() ： 去除字符串右边的空格
conv = lambda s: dt.datetime.strptime(s.lstrip( ).rstrip( ), '%Y-%m-%d %H:%M:%S.%f')


#print data

#Use numpy to read the data in. 
#    0        1            2             3                  4                       5                      6                           7                           8                      9                        10                              11                  12                          13                    14                          15                      16                     17                     18                      19                    20                      21                        22
#Num. | OriginFcId | RestoreFcId | trafficId |        StartTime        |         EndTime    |  ReCreateResourcesStartTime | ReCreateResourcesEndTime |  RouteRequestStartTime  |   RouteRequestEndTime     |     RouteStartTime      |      RouteEndTime       | ResourcesStartTime    |    ResourcesEndTime     |    XcMethodStartTime    |     XcMethodEndTime       CrossStartTime      |   CrossingTime   |     CrossEndTime       |   Alarm Occured Time    | Restore Wait Time |  RestoreWaitStartTime   |   RestoreWaitEndTime 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
data = np.genfromtxt(a, delimiter="|", converters={4: conv,   5: conv,  6: conv,  7: conv,  8: conv,  9: conv,  10: conv,  11: conv,  12: conv,  13: conv,  14: conv,  15: conv,  16: conv,  17: conv,  18: conv, 19: conv},
                     names=['Num', 'OriginFcId', 'RestoreFcId', 'trafficId', 'StartTime', 
                            'EndTime','ReCreateResourcesStartTime', 'ReCreateResourcesEndTime', 'RouteRequestStartTime', 'RouteRequestEndTime', 
                            'RouteStartTime', 'RouteEndTime', 'ResourcesStartTime', 'ResourcesEndTime', 'XcMethodStartTime', 
                            'XcMethodEndTime', 'CrossStartTime','CrossingTime', 'CrossEndTime', 'AlarmOccuredTime', 
                            'RestoreWaitTime', 'RestoreWaitStartTime', 'RestoreWaitEndTime'], 
                            dtype=None)

#print data



Num, OriginFcId, RestoreFcId, trafficId, StartTime, EndTime,ReCreateResourcesStartTime, ReCreateResourcesEndTime, RouteRequestStartTime, RouteRequestEndTime, RouteStartTime, RouteEndTime, ResourcesStartTime, ResourcesEndTime, XcMethodStartTime, XcMethodEndTime, CrossStartTime, CrossingTime, CrossEndTime, AlarmOccuredTime, RestoreWaitTime, RestoreWaitStartTime, RestoreWaitEndTime = data['Num'], data['OriginFcId'], data['RestoreFcId'], data['trafficId'], data['StartTime'], data['EndTime'], data['ReCreateResourcesStartTime'], data['ReCreateResourcesEndTime'], data['RouteRequestStartTime'], data['RouteRequestEndTime'], data['RouteStartTime'], data['RouteEndTime'], data['ResourcesStartTime'], data['ResourcesEndTime'], data['XcMethodStartTime'], data['XcMethodEndTime'], data['CrossStartTime'], data['CrossingTime'], data['CrossEndTime'] , data['AlarmOccuredTime'], data['RestoreWaitTime'], data['RestoreWaitStartTime'] ,data['RestoreWaitEndTime']


#Get unique captions and there indices and the inverse mapping
captions, unique_idx,Num_inv = np.unique(Num, 1, 1)

#Build y values from the number of unique captions.
y = (Num_inv + 1) / float(len(captions) + 1)


#Plot function
def timelines(y, xStartTime, xEndTime, xReCreateResourcesStartTime, xReCreateResourcesEndTime, xRouteRequestStartTime, xRouteRequestEndTime,xRouteStartTime, xRouteEndTime, xResourcesStartTime, xResourcesEndTime, xXcMethodStartTime, xXcMethodEndTime,xCrossStartTime, xCrossingTime, xCrossEndTime, xAlarmOccuredTime, xRestoreWaitStartTime, xRestoreWaitEndTime):
    """Plot timelines at y from xstart to xstop with given color."""  
    #划横线 
    #blue  
    #g  green  
    #y    yellow
    #k    black
    #‘b’    blue 蓝色：xAlarmOccuredTime——>xRestoreWaitStartTime 从告警产生到恢复等待开始
    #‘y’    yellow 黄色：xRestoreWaitStartTime——>xRestoreWaitEndTime 从恢复等待开始到恢复等待结束
    #‘g’    green 蓝色：xRestoreWaitEndTime-->xRouteStartTime,从恢复等待结束到开始路由
    #‘r’    red 红色:xRouteStartTime-->xRouteEndTime,从发起算路到返回路由结果
    #‘c’    cyan 青色 :xRouteEndTime-->xCrossStartTime,从路由结束到开始下交叉
    #‘m’    magenta 从下发交叉开始到收到所有交叉响应
    #'lightblue':            '#ADD8E6',
    #'goldenrod':            '#DAA520',
    #'darksalmon':           '#E9967A'
    #'seashell':             '#FFF5EE',
    #'fuchsia':              '#FF00FF',
    #'hotpink':              '#FF69B4',
    #'darkgray':             '#A9A9A9',
    #'limegreen':            '#32CD32',
    #'burlywood':            '#DEB887',
    #https://www.cnblogs.com/darkknightzh/p/6117528.html
    ret1 = plt.hlines(y, xAlarmOccuredTime, xStartTime, 'b', lw=2)
    #plt.hlines(y, xAlarmOccuredTime, xRestoreWaitStartTime, 'b', lw=2)
    #plt.hlines(y, xRestoreWaitStartTime, xRestoreWaitEndTime, 'y', lw=2)
    ret2 = plt.hlines(y, xStartTime, xReCreateResourcesStartTime, 'g', lw=2)
    ret3 = plt.hlines(y, xReCreateResourcesStartTime, xReCreateResourcesEndTime, 'lightblue', lw=2)
    ret4 = plt.hlines(y, xReCreateResourcesEndTime, xRouteRequestStartTime, 'goldenrod', lw=2)
    ret5 = plt.hlines(y, xRouteRequestStartTime, xRouteRequestEndTime, 'darksalmon', lw=2)
    ret6 = plt.hlines(y, xRouteRequestEndTime, xRouteStartTime, 'seashell', lw=2)
    ret7 = plt.hlines(y, xRouteStartTime, xRouteEndTime, 'r', lw=2)
    ret8 = plt.hlines(y, xRouteEndTime, xResourcesStartTime, 'fuchsia', lw=2)
    ret9 = plt.hlines(y, xResourcesStartTime, xResourcesEndTime, 'hotpink', lw=2)
    ret10 = plt.hlines(y, xResourcesEndTime, xXcMethodStartTime, 'darkgray', lw=2)
    ret11 = plt.hlines(y, xXcMethodStartTime, xXcMethodEndTime, 'limegreen', lw=2)
    ret12 = plt.hlines(y, xXcMethodEndTime, xCrossStartTime, 'burlywood', lw=2)
    ret13 = plt.hlines(y, xCrossStartTime, xCrossingTime, 'r', lw=2)
    ret14 = plt.hlines(y, xCrossingTime, xCrossEndTime, 'm', lw=2)
    #xResourcesEndTime, xXcMethodStartTime, xXcMethodEndTime,xCrossStartTime
    #截止线
    plt.vlines(xAlarmOccuredTime, y+0.001, y-0.001, 'k', lw=1)
    plt.vlines(xStartTime, y+0.001, y-0.001, 'k', lw=1)
    plt.vlines(xRouteStartTime, y+0.001, y-0.001, 'k', lw=1)
    plt.vlines(xRouteEndTime, y+0.001, y-0.001, 'k', lw=1)
    plt.vlines(xCrossStartTime, y+0.001, y-0.001, 'k', lw=1)
    plt.vlines(xCrossEndTime, y+0.001, y-0.001, 'k', lw=1)
    return (ret1, ret2,ret3, ret4, ret5, ret6, ret7, ret8, ret9, ret10, ret11, ret12, ret13, ret14)

#Plot time line   
ret = timelines(y, StartTime,EndTime,ReCreateResourcesStartTime,ReCreateResourcesEndTime,RouteRequestStartTime,RouteRequestEndTime,RouteStartTime,RouteEndTime,ResourcesStartTime,ResourcesEndTime,XcMethodStartTime,XcMethodEndTime,CrossStartTime,CrossingTime,CrossEndTime,AlarmOccuredTime,RestoreWaitStartTime,RestoreWaitEndTime)


#Setup the plot
ax = plt.gca()
# 设置中文支持方式
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
ax.xaxis_date()
myFmt = DateFormatter('%H:%M:%S.%f')
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.set_major_locator(SecondLocator(interval=1)) # 设置为1S间隔
# 设置X轴坐标字体和显示方式
plt.xticks(fontsize=8, color="black", rotation=-90)

txt = u"blue:xAlarmOccuredTime-->xStartTime"\
    u"green:xStartTime-->xRouteStartTime"\
    u"red:xRouteStartTime-->xRouteEndTime"\
    u"cyan:xRouteEndTime-->xCrossStartTime"\
    u"magenta:xCrossStartTime-->CrossEndTime"\


plt.text(5, 10, txt, fontsize=18, style='oblique', ha='center',va='top',wrap=True)

plt.legend(ret,
           ('xAlarmOccuredTime-->xStartTime',
            'xStartTime-->xReCreateResourcesStartTime',
            'xReCreateResourcesStartTime-->xReCreateResourcesEndTime',
            'xReCreateResourcesEndTime-->xRouteRequestStartTime',
            'xRouteRequestStartTime-->xRouteRequestEndTime',
            'xRouteRequestEndTime-->xRouteStartTime',
            'xRouteStartTime-->xRouteEndTime',
            'xRouteEndTime-->xResourcesStartTime',
            'xResourcesStartTime-->xResourcesEndTime',
            'xResourcesEndTime-->xXcMethodStartTime',
            'xXcMethodStartTime-->xXcMethodEndTime',
            'xXcMethodEndTime-->xCrossStartTime',
            'xCrossStartTime-->xCrossingTime',
            'xCrossingTime-->CrossEndTime', ))


#To adjust the xlimits a timedelta is needed.
delta = (EndTime.max() - AlarmOccuredTime.min())

#print delta
print "AlarmOccuredTime.min:" 
print  AlarmOccuredTime.min()

print "AlarmOccuredTime.max:" 
print  AlarmOccuredTime.max()

print '''\r\n'''

print "RouteStartTime.min:" 
print  RouteStartTime.min()

print "RouteStartTime.max:" 
print  RouteStartTime.max()

print '''\r\n'''

print "RouteEndTime.min:" 
print  RouteEndTime.min()

print "RouteEndTime.max:" 
print  RouteEndTime.max()

print '''\r\n'''


print "CrossStartTime.min:" 
print CrossStartTime.min()

print "CrossStartTime.max:" 
print CrossStartTime.max()

print '''\r\n'''

plt.xlabel(u'时间')
plt.ylabel(u'序号')
plt.title(u'控制器性能分析')
plt.yticks(y[unique_idx], captions)
plt.ylim(0,1)
#设置当年X轴显示范围
plt.xlim(AlarmOccuredTime.min(), EndTime.max())
#plt.xlabel('Time')
#设置X轴标度线
ax.xaxis.grid(True, which='major')
plt.show()
# plt.savefig('ControllerPerformance' + dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.png')
