from argparse import ArgumentParser
from time import sleep
from src.testArgument import testAllArguments, init
from src.CLI import printBanner, printError, printResult, avancement, resetLine, printInfo
from src.testConnection import testSubdomains
from gevent.queue import Queue
from gevent import spawn, joinall
import timeit

_NB_SUBD = 0
_AVANCEMENT = 0
_TASKS = Queue()
_MAX = 0
_R_N = 1
_LENGTH = 0
_b_nm = 1
_OPTI = False

def init_queue(p_domains,r):
    global _MAX
    global _LENGTH
    global _OPTI
    global _R_N

    domainArray = []
    tmpArray = []
    _MAX = len(p_domains)
    for d_id in range(_MAX):
        d = possible_subdomains[d_id]
        url = d +"."+testingDomain
        tmpArray.append(url)

    domainArray.append(tmpArray)
    if _R_N > 1 and not _OPTI:
        while len(domainArray) < _R_N:
            tmpArray = []
            lastDomainId = len(domainArray)-1
            for domain in domainArray[lastDomainId]:

                for d_id in range(_MAX):
                    d = possible_subdomains[d_id]
                    url = d +"."+domain
                    tmpArray.append(url)
            domainArray.append(tmpArray)
    for rLevel in domainArray:
        for url in rLevel:
            _TASKS.put_nowait(url)


    _LENGTH = _MAX

def threadFunction():
    global _AVANCEMENT
    global _NB_SUBD
    global _R_N
    global _MAX
    global _LENGTH
    global _b_nm
    global _OPTI

    while not _TASKS.empty():
        domain_name = _TASKS.get()
        _AVANCEMENT = _AVANCEMENT +1
        avancement( _AVANCEMENT, _LENGTH, _MAX)
        hasResult, status = testSubdomains(domain_name)
        if hasResult:
            _NB_SUBD = _NB_SUBD + 1
            printResult(status, domain_name)
            if _OPTI:
                d_array = domain_name.split(".")
                if len(d_array) < (_b_nm + _R_N) and  d_array[0] != "www":
                    for d_id in range(_MAX):
                        d = possible_subdomains[d_id]
                        url = d +"."+domain_name
                        _TASKS.put_nowait(url)
                    _LENGTH = _LENGTH + _MAX


if __name__ == '__main__':
    parser = ArgumentParser(description="Description heres")
    parser.add_argument('-u', '--url', required=True, help="the url you want to test")
    parser.add_argument('-w', '--wordlist', required=False, help="")
    parser.add_argument('-r', '--recursive',type=int, required=False, help="")
    parser.add_argument('-t', '--thread',type=int, required=False, help="(int) The number of threads you wish to perform")
    parser.add_argument('--optimize',action='store_true', required=False, help="")

    printBanner()

    arguments = parser.parse_args()
    isOk, infos = testAllArguments(arguments)

    if not isOk:
        exit(1)

    testingDomain,wordlist,_R_N,nbThread, _OPTI = init(infos)
    _b_nm = len(testingDomain.split("."))
    possible_subdomains = open(wordlist,'r').read().split("\n")
    spawn(init_queue,possible_subdomains, _R_N).join()
    start = timeit.default_timer()
    tArray = []
    for t in range(nbThread):
        tArray.append(spawn(threadFunction))
    joinall(tArray)

    resetLine()
    print()
    printInfo("There are %s subdomains for the links %s" % (_NB_SUBD,testingDomain))
    stop = timeit.default_timer()
    printInfo("Compute duration : %s " % (stop - start))
