# -*- coding: cp936 -*-
import os,sys
import xlrd
from pychart import *
#import xlwt
#import pyExcelerator

#if __name__ == __main__ :
    
fname = "待构建变更活动.xls"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("Sheet1")
except:
    print "no sheet in %s named Sheet1" % fname
#    return None
'''
nrows = sh.nrows
ncols = sh.ncols
print "nrows %d, ncols %d" % (nrows,ncols)
 
cell_value = sh.cell_value(1,1)
print cell_value

 
row_list = []
for i in range(1,nrows):
    row_data = sh.row_values(i)
    row_list.append(row_data)
'''

for s in bk.sheets():
    print 'Sheet:',s.name
    nrows = sh.nrows
    ncols = sh.ncols
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
            values.append(s.cell(row,col).value)
        print ','.join(values)
    print
'''
wb = Workbook()
ws = wb.add_sheet(‘result’)
ws.write(0,0,“hello”)
wb.save(‘result.xls’
'''
