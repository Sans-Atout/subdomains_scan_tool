from time import localtime, strftime
from shutil import get_terminal_size

# Define nice print function
_BASE_COLOR = "\033["
_RED = _BASE_COLOR+"31m"
_GREEN = _BASE_COLOR+"32m"
_YELLOW = _BASE_COLOR+"33m"
_BLUE = _BASE_COLOR+"34m"
_PURPLE = _BASE_COLOR+"35m"
_LBLUE = _BASE_COLOR+"36m"
_WHITE = _BASE_COLOR+"37m"
_RESET = _BASE_COLOR+"0m"

_BANNER = '''
\t================================
\t|                              |
\t|  Subdomains detection tools  |
\t|        version 1.0.2         |
\t|                              |
\t================================
'''

def getBaseLog():
    return "["+getFormatedDate()+"]\t"

def getFormatedDate():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def printBanner():
    print(_YELLOW + _BANNER+_RESET)

def printInfo(log):
    print(getBaseLog()+_LBLUE+"[INFO\t]\t"+_RESET+str(log))

def printInit(domains, thread,wordlist):
    print("\tdomains tested\t\t: "  +domains+_RESET)
    print("\tnumber of treath(s)\t: "  +str(thread)+_RESET)
    print("\twordlist path\t\t: "  +wordlist+_RESET)


def printFatal(log):
    print(getBaseLog()+_RED+"[FATAL\t]\t"+_RESET+str(log))
    exit(1)

def printResult(status,url):
    resetLine()
    log = _RESET + getBaseLog()+"["
    if status >= 200 and status < 300:
        log = log +_GREEN+str(status)
    elif status >= 300 and status < 400:
        log = log +_YELLOW+str(status)
    else:
        log = log +_RED+str(status)
    log = log+_RESET+']\t'+str(url)
    print("\r"+log)
    
def printError(log):
    print(getBaseLog()+_RED+"[ERROR\t]\t"+_RESET+str(log))
    print()

def getBaseLog():
    return "["+getFormatedDate()+"]\t"

def getFormatedDate():
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def avancement(prcent,after="*"):
    length = 33
    before="*"
    empty = "-"
    bar = "["
    full = "#"
    for i in range(length):
        if i <= prcent / (100/length):
            bar = bar + full
        else:
            bar = bar + empty
    bar = bar + "]"
    print("\r"+getBaseLog()+_YELLOW+bar+" "+"{:.2%}".format(prcent/100) +"\t["+after+"]", end ="")

def resetLine():
    columns, lines = get_terminal_size()
    print("\r"+" "*(columns-1),end='')