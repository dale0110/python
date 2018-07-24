#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#

import paramiko
import socket
import logging
import select
import time
import re
import json
import requests

logger = logging.getLogger(__name__)


recv_buffer_size = 10000

SSH_ENDING=""

def run_command (command, host='127.0.0.1'):
    #print command
    #print "connectting... ..."
    logger.info('connectting %s', host)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.connect((host, 8101))
    except paramiko.AuthenticationException:
        print "Authentication failed when connecting to %s" % host
    except socket.error, e:
        raise IOError(
        'could not connect to the ssh server: \n {0} \n {1}'.format(host, e))
    except paramiko.ssh_exception.AuthenticationException, e:
        raise IOError(
        'username or password authentication error \n {0}'.format(e))
    except Exception, e:
        raise IOError('error connecting to server: \n {0}'.format(e))
    
    trans = paramiko.Transport(s)
    trans.set_keepalive(1)
    trans.start_client()
    trans.auth_password("karaf", "karaf")
    channel = trans.open_session()
    channel.get_pty()
    channel.settimeout(2)
    print "connect %s OK"
    logger.info('connect %s OK', host)

    channel.invoke_shell()

    data = channel.recv(recv_buffer_size)
    
    #while len(data) > 0 and not data.endswith('@root> '):
     #   print data
     #   print len(data)
     #   data += channel.recv(recv_buffer_size)
    
    print data


    logger.info('sendding  %s ', command)
    print 'sendding '+ command
    channel.send(command + '\n')
    
    
    channel.settimeout(5)
    data = ''
    
    #while not channel.exit_status_ready():
    # Only print data if there is data to read in the channel
    #    if channel.recv_ready():
    #        rl, wl, xl = select.select([channel], [], [], 0.0)
    #        if len(rl) > 0:
    #            # Print data from stdout
    #            data += channel.recv(recv_buffer_size),
        
    time.sleep(5)
        
    while True:
        if channel.exit_status_ready():
            break
        rl, wl, xl = select.select([channel], [], [], 0.0)
        if len(rl) > 0:
            data += channel.recv(recv_buffer_size)
            #print data
        elif len(rl) == 0  :
            break
    
    print data
    
    
    channel.send('logout\n')
    
    channel.recv_exit_status()
    channel.close()
    trans.close()

    return data



def get_state (host='localhost',ALLBundleNum=0, NoActiveBundleNum=0,OTNBundleNum=0):
    print 'run_command... ...'
    
    #发送list命令
    output = run_command('list', host)
    #print output

    #分割每行
    lines=output.split('\n')
    #print len(lines)
        
    #分析输出结果，生成列表，列表的元素为由每个bundle的信息组成的元组（）('ID', 'State', 'Lvl', 'Version') 
    #R3B10版本 velcome正常数量为359+1
    bundlelist=[]    
    for line in lines:
        #创建词典
        bundle = {}
        fields = line.split('|')
        try:
            #fields[0]:id; fields[1]:状态;fields[2]:unkown;fields[3]:版本；fields[4]:名称
            #('ID', 'State', 'Lvl', 'Version')
            #增加列表元素
            bundlelist.append((fields[0].strip() ,fields[1].strip(),fields[2].strip(),fields[3].strip(),fields[4].strip()))
            #print  fields[0].strip() + fields[1].strip()+fields[2].strip()+fields[3].strip()+fields[4].strip() 
        except:
            pass
    
    #生成非 Active的模块列表，正常状态为下面内容
    #('ID', 'State', 'Lvl', 'Version', 'Name')
    #('14', 'Resolved', '20', '1.0.0', 'Apache Aries Blueprint Core Compatiblity Fragment Bundle, Hosts: 15')
    #('99', 'Resolved', '80', '0.4.4.2_00_10R3B10', 'com.zte.sdn.oscp.controller.config-persister-file-xml-adapter, Hosts: 100')
    #('188', 'Resolved', '30', '1.0.0.v20110524', 'Region Digraph')
    #('189', 'Resolved', '30', '3.0.3', 'Apache Karaf :: Region :: Persistence')
    NoActiveBundleList=[]
    OTNBundleList=[] 
    for bundle in bundlelist:
        
        #生成非 Active的模块列表，正常状态为下面内容
        if cmp(bundle[1],"Active")!=0:
            #print bundle
            NoActiveBundleList.append(bundle)
        #生成otn bundlelist
        if len(re.findall("otn",bundle[4]))>0:
            OTNBundleList.append(bundle)
            print bundle
    
    if len(NoActiveBundleList)!=(NoActiveBundleNum+1):
        print NoActiveBundleList
    
    if len(OTNBundleList)!=OTNBundleNum:
        print len(OTNBundleList)
        print OTNBundleList
    
    if len(bundlelist)!=(ALLBundleNum+1):
        print len(bundlelist)
        print bundlelist



logger.info('start... ...')
print "start... ..."

    #生成非 Active的模块列表，正常状态为下面内容
    #('ID', 'State', 'Lvl', 'Version', 'Name')
    #('14', 'Resolved', '20', '1.0.0', 'Apache Aries Blueprint Core Compatiblity Fragment Bundle, Hosts: 15')
    #('99', 'Resolved', '80', '0.4.4.2_00_10R3B10', 'com.zte.sdn.oscp.controller.config-persister-file-xml-adapter, Hosts: 100')
    #('188', 'Resolved', '30', '1.0.0.v20110524', 'Region Digraph')
    #('189', 'Resolved', '30', '3.0.3', 'Apache Karaf :: Region :: Persistence')
    #总共360个bundle，otn的bundle数量为33
print get_state('10.85.160.13',360,4,33)

