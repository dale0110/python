from socket import *
tgtHost=raw_input("What is the web address?: ")
tgtPorts=raw_input("What are the ports seperated by commas? or would you like to test all?: ")
def connScan(tgtHost, tgtPort):
    try:
        connSkt=socket(AF_INET, SOCK_STREAM)
        connSkt.settimeout(10)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.settimeout(None)
        print("%d/tcp open"%tgtPort)
    except:
        print("%d/tcp closed"%tgtPort)
def portScan(tgtHost, tgtports):
    global tgtPorts
   
    if  tgtPorts=="yes" or tgtPorts=="ya" or tgtPorts=="sure" or tgtPorts=="ok" or tgtPorts=="y" or tgtPorts=="Y":
         tgtPorts=21, 22, 23, 25, 42, 43, 53, 67, 79, 80, 102, 110, 115, 119, 123, 135, 137, 143, 161, 179, 379, 389, 443, 445, 465, 636, 993, 995, 1026, 1080, 1090, 1433, 1434, 1521, 1677, 1701, 1720, 1723, 1900, 2409, 3101, 3306, 3389, 3390, 3535, 4321, 4664, 5190, 5500, 5631, 5632, 5900, 7070, 7100, 8000, 8080, 8799, 8880, 9100, 19430, 39720
   
   
    try:
        tgtIP=gethostbyname(tgtHost)
    except:
        print(" Cannot resolve '%s': Unknown host"%tgtHost)
        return
    try:
        tgtName=gethostbyaddr(tgtIP)
        print('\n Scan results for: %s' %tgtName)
    except:
        print('\n Scan results for: %s' %tgtIP)
    tgtPorts=tgtPorts.split(',')
    for port in tgtPorts:
        print('Scanning port %s'%port)
        connScan(tgtHost, int(port))
def main():
    portScan(tgtHost, tgtPorts)
if __name__=='__main__':
    main()
 
#该代码片段来自于: http://www.sharejs.com/codes/python/8449
