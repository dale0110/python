import mechanize
import sys

def usage():
    print "Usage: python" + ' ' + sys.argv[0] + ' ' + "<url>"
    sys.exit()

def reloader():
    br = mechanize.Browser()
    reload_count = 0
    #url = sys.argv[1]
    url = 'http://www.python.org'
    start = br.open(url)

    while True:
        try:
            br.reload()
            reload_count += 1
            print "[+] Sent reload request", "%s" % (reload_count)
        except KeyboardInterrupt:
            sys.exit("\nProcess aborted.")
'''
if len(sys.argv) < 2:
    usage()
'''
if __name__ == "__main__":
    reloader()
