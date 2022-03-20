from time import localtime, strftime
from shutil import get_terminal_size

from colorama import init
from colorama import Fore, Style
init()

_COLOR = {
        'INFO': Style.BRIGHT + Fore.BLUE,
        'UNKNOW': Style.BRIGHT + Fore.MAGENTA,
        'OK': Style.BRIGHT + Fore.GREEN,
        'GREY' : Style.BRIGHT + Fore.LIGHTBLACK_EX,
        'YELLOW': Style.BRIGHT + Fore.YELLOW,
        'ERROR': Style.BRIGHT + Fore.RED,
        'DEFAULT': Style.BRIGHT + Fore.WHITE,
        'END': Style.RESET_ALL,
    }

_BANNER = '''
\t================================
\t|                              |
\t|  Subdomains detection tools  |
\t|        version 1.0.5         |
\t|                              |
\t================================
'''
def setColor(cName):
    return _COLOR[cName]

_D_FORMAT = setColor("GREY")+"%Y-%m-%d %H:%M:%S"+setColor("END")

def getBaseLog():
    return setColor("END")+"["+getFormatedDate()+"]\t"

def getFormatedDate():
    return strftime( _D_FORMAT, localtime())

def printBanner():
    print(setColor("YELLOW") + _BANNER+setColor("END"))


def printInit(domains, thread,wordlist, recursive, optimize):
    print()
    printInfo("domains tested\t\t: "  +domains)
    printInfo("wordlist path\t\t: "  +wordlist)
    printInfo("number of treath(s)\t: "  +str(thread))
    printInfo("recursivity level\t: "  +str(recursive))
    printInfo("optimize\t\t: %s" % str(optimize))
    return


def printFatal(log):
    print(getBaseLog()+_RED+"[FATAL\t]\t"+setColor("END")+str(log))
    exit(1)

def printResult(status,url):
    resetLine()
    log = getBaseLog()+"["
    if status >= 200 and status < 300:
        log = log +setColor("OK")+str(status)
    elif status >= 300 and status < 400:
        log = log +setColor("YELLOW")+str(status)
    elif status == -2:
        log = log +setColor("UNKNOW")+'000'
    else:
        log = log +setColor("ERROR")+str(status)
    log = log+setColor("END")+']\t'+str(url)
    print("\r"+log)

def printError(log):
    print(getBaseLog()+setColor("ERROR")+"[ERROR\t]\t"+setColor("END")+str(log))

def avancement(done, max, t_len):

    t_nb = done // t_len
    p_nb = done % t_len
    prcent = 100 * (p_nb + 1) / t_len
    max_t = int(max/t_len)
    f = ">"+str(len(str(max_t)))
    f_t = ">"+str(len(str(t_len)))
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
    pourcentage = format("{:.2%}".format(prcent/100), ">7")
    ligne = "\r"+getBaseLog()+setColor("YELLOW")+bar+" "+pourcentage+ "  "
    ligne = ligne + "["+format(t_nb,f)+"/"+str(max_t)+"]  ["+format(p_nb,f_t)
    ligne = ligne + "/"+str(t_len)+"]"+setColor("END")
    print(ligne, end ="")

def resetLine():
    columns, lines = get_terminal_size()
    print("\r"+" "*(columns-1),end='')

def printWarning(log):
    print(getBaseLog()+setColor("YELLOW")+"[WARNING]\t"+setColor("END")+str(log))

def printInfo(log):
    print(getBaseLog()+setColor("INFO")+"[INFO\t]\t"+setColor("END")+str(log))
