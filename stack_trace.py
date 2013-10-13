import traceback

def fifths(a):
    return 5/a

def myfunction(value):
    b = fifths(value) * 100

try:
    print myfunction(0)
except Exception, ex:
    logfile = open('mylog.log','a')
    traceback.print_exc(file=logfile)
    logfile.close()
    print "Oops ! Something went wrong. Please look in the log file."
