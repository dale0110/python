# coding=utf-8


import thread
import string
import platform
import logging
import os,sys, socket, struct, select, time


if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8 # Seems to be the same on Solaris.


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    sum = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count<countTo:
        thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff # Necessary?
        count = count + 2

    if countTo<len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff # Necessary?

    sum = (sum >> 16)  +  (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, ID, timeout):
    """
    receive the ping from the socket.
    """
    timeLeft = timeout
    while True:
        startedSelect = default_timer()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] == []: # Timeout
            return

        timeReceived = default_timer()
        recPacket, addr = my_socket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
        # Filters out the echo request itself. 
        # This can be tested by pinging 127.0.0.1 
        # You'll see your own request
        if type != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return


def send_one_ping(my_socket, dest_addr, ID):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr  =  socket.gethostbyname(dest_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", default_timer()) + data

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
    )
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1)) # Don't know about the 1


def do_one(dest_addr, timeout):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (errno, msg):
        if errno == 1:
            # Operation not permitted
            msg = msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(msg)
        raise # raise the original error

    my_ID = os.getpid() & 0xFFFF

    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, my_ID, timeout)

    my_socket.close()
    return delay


def verbose_ping(dest_addr, timeout = 2, count = 4):
    """
    Send >count< ping to >dest_addr< with the given >timeout< and display
    the result.
    """
    ping_result=False
    for i in xrange(count):
        print "ping %s..." % dest_addr,
        try:
            delay  =  do_one(dest_addr, timeout)
        except socket.gaierror, e:
            print "failed. (socket error: '%s')" % e[1]
            break

        if delay  ==  None:
            print "failed. (timeout within %ssec.)" % timeout
            ping_result=False
        else:
            delay  =  delay * 1000
            print "get ping in %0.4fms" % delay
            ping_result=True
    return ping_result

ftplogger=0


def logger_init():
      
    ''' 创建一个logger ''' 
    logger = logging.getLogger('pinglogger')  
    logger.setLevel(logging.DEBUG)  
      
    ''' 创建一个handler，用于写入日志文件 '''
    fh = logging.FileHandler('ping.log')  
    fh.setLevel(logging.DEBUG)  
      
    '''再创建一个handler，用于输出到控制台  '''
    ch = logging.StreamHandler()  
    ch.setLevel(logging.DEBUG)  
      
    ''' 定义handler的输出格式  '''
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d- %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  
    ch.setFormatter(formatter)  
      
    ''' 给logger添加handler  '''
    logger.addHandler(fh)  
    logger.addHandler(ch)
    return  logger


def isUp(hostname):
    global ftplogger
    
    giveFeedback = True

    if verbose_ping(hostname) == True:
        print hostname, 'is up!'
        ftplogger.info(hostname+':UP')
    else:
        print hostname, 'is down!'
        ftplogger.info(hostname+':DOWN')


def isUp2(hostname):
    global ftplogger
    
    giveFeedback = True

    if platform.system() == "Windows":
        response = os.system("ping "+hostname+" -n 4")
    else:
        response = os.system("ping -c 4 " + hostname)

    isUpBool = False
    if response == 0:
        if giveFeedback:
            print hostname, 'is up!'
            ftplogger.info(hostname+':UP')
        isUpBool = True
    else:
        if giveFeedback:
            print hostname, 'is down!'
            ftplogger.info(hostname+':DOWN')

    return isUpBool



#通过读取配置文件上载ftp文件
def main():
    global ftplogger
    ftplogger=logger_init()
    ftplogger.info("start ping test")
    try:
        configfile = open("config.ini",'r')
        while 1: 
            message=configfile.readline()
            if len(message)< 10:
                break
            list1=message.split()
            print "host="+list1[0]
            host=list1[0]
            if not ( host=="") :
                isUp2(str(host))
            else :
                print "configfile error"
        configfile.close()
    except Exception,ex:
        print Exception,":",ex
    ftplogger.info("test end")
    return 0

#-------------------------------------------------------------------------------
if __name__ == '__main__':
        main()
