from argparse import ArgumentParser
from time import sleep
from src.testArgument import testAllArguments, init
from src.CLI import printBanner, printError, printResult, avancement, resetLine
from src.testConnection import testSubdomains
from gevent.queue import Queue
from gevent import spawn, joinall

_NB_SUBD = 0
_AVANCEMENT = 0
_TASKS = Queue()
_MAX = 0

def init_queue(p_domains):
    global _MAX 
    _MAX = len(p_domains)
    for d_id in range(_MAX):
        d = possible_subdomains[d_id]
        url = d +"."+testingDomain
        _TASKS.put_nowait(url)

def threadFunction():
    global _AVANCEMENT
    global _NB_SUBD
    while not _TASKS.empty():
        domain_name = _TASKS.get()
        _AVANCEMENT = _AVANCEMENT +1
        avancement( 100 * _AVANCEMENT/_MAX, str(_AVANCEMENT) +'/'+str(_MAX))
        hasResult, status = testSubdomains(domain_name)
        if hasResult:
            _NB_SUBD = _NB_SUBD + 1
            printResult(status, domain_name)

if __name__ == '__main__':
    parser = ArgumentParser(description="Description heres")
    parser.add_argument('-u', '--url', required=True, help="the url you want to test")
    parser.add_argument('-w', '--wordlist', required=False, help="")
    parser.add_argument('-r', '--recursive',type=int, required=False, help="")
    parser.add_argument('-t', '--thread',type=int, required=False, help="(int) The number of threads you wish to perform")

    printBanner()

    arguments = parser.parse_args()
    isOk, infos = testAllArguments(arguments)

    if not isOk:
        exit(1)

    testingDomain,wordlist,r,nbThread = init(infos)
    possible_subdomains = open(wordlist,'r').read().split("\n")
    spawn(init_queue,possible_subdomains).join()
    tArray = []
    for t in range(100):
        tArray.append(spawn(threadFunction))
    joinall(tArray)
    
    resetLine()
    print()
    print("There are %s subdomains for the links %s" % (_NB_SUBD,testingDomain))
