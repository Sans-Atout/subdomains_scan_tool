# Load usefull librairie

## multi-threading librairie
from gevent.queue import Queue
from gevent import spawn, joinall
from src.CLI import printResult, resetLine, avancement
from src.testConnection import testSubdomains
# Globale variable use in this script
_optimize = False
_baseSubDomain = 1
_length = 0
_recursiveNb = 1
_pLength = 0
_tasks = Queue()
_avancement = 0
_subDLevel = 0
_nbSubD = 0
_threadNb = 1
_pSubDomains = [] # All possible subdomains according to wordlist file
_mainDomain = "example.com" # the main domain to test

def getNbSubD():
    global _nbSubD
    return _nbSubD

def loadPSubD(path):
    global _pSubDomains
    _pSubDomains = open(path, 'r').read().split('\n')
    return

def initScan(d,w,r,t,o):
    # def of all global variable
    global _mainDomain
    global _recursiveNb
    global _threadNb
    global _optimize
    global _baseSubDomain
    # global variable set
    _mainDomain = d
    _recursiveNb = r
    _threadNb = t
    _optimize = o
    loadPSubD(w)
    _baseSubDomain = len(d.split("."))
    spawn(queueInitialisation).join()
    return

def queueInitialisation():
    # def of all global variable
    global _pLength
    global _length
    global _recursiveNb
    global _optimize
    global _pSubDomains
    global _mainDomain
    global _tasks

    allDomains = []
    tmpDomains = []
    _length = len(_pSubDomains)
    # first init
    for dId in range(_length):
        d2Test = _pSubDomains[dId] + '.' + _mainDomain
        tmpDomains.append(d2Test)
    allDomains.append(tmpDomains)
    _pLength = _length

    # If the recursive is greater than 1 and opti is disable; we had all possible
    # subdomains in the queue
    if (not _optimize) and (_recursiveNb > 1):
        while len(allDomains) < _recursiveNb:
            tmpDomains = []
            lDomainId = len(allDomains) - 1
            for topLevelDomain in allDomains[lDomainId]:
                for _id in range(_pLength):
                    d = _pSubDomains[_id]
                    u = d +'.'+topLevelDomain
                    tmpDomains.append(u)
            allDomains.append(tmpDomains)

    # add all level to queue:
    for rLvl in allDomains:
        for u in rLvl:
            _tasks.put_nowait(u)
        _pLength = _pLength + _length
    return

def startScript():
    global _threadNb
    print()
    allThread = []
    while len(allThread) < _threadNb:
        allThread.append(spawn(thread))
        #print(len(allThread))
    joinall(allThread)
    #resetLine()
    print()

def thread():
    # def of all global variable
    global _avancement
    global _tasks
    global _pLength
    global _length
    global _baseSubDomain
    global _optimize
    global _recursiveNb
    global _pSubDomains
    global _nbSubD

    # On récupère un domain tant que les tasks ne sont pas fini
    while not _tasks.empty():
        domainToTest = _tasks.get()
        _avancement = _avancement + 1
        avancement(_avancement, _pLength,_length )
        hasResult, resStatus = testSubdomains(domainToTest)
        # if the tested result have a record in DNS server we print it
        if hasResult:
            _nbSubD = _nbSubD + 1
            printResult(resStatus, domainToTest)
            # if the opti flag is set and we have to add the other sub domains to
            # test
            if _optimize:
                domains = domainToTest.split(".")
                # If the smallest sub-level domain is not equal to "www" (usually
                # the last possible sub-domain) and if the maximum recursion level
                # requested by the user is not reached then sub-domains are
                # added to the queue
                if len(domains) < (_baseSubDomain + _recursiveNb) and domains[0] != "www":
                    for subD in _pSubDomains:
                        u = subD + "."+domainToTest
                        _tasks.put_nowait(u)
                    _pLength = _pLength + _length
    return
