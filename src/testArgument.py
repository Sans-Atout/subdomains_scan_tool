from src.CLI import printError, printWarning, printInit
from re import search
from os.path import exists

lookLikeDomainRegex = "([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}"

def testAllArguments(arguments):
    info = {}
    is_valid, domain = isAValidDommainName(arguments.url)
    if not is_valid:
        return (False,{"domain" : (False, "Unkown domain") })
    info["domain"] = (True, domain)

    if arguments.wordlist != None:
        is_valid_wl, wl = isAValidWorlList(arguments.wordlist)
        info["wordlist"] = (is_valid_wl, wl)
    else:
        info["wordlist"] = (False, "")

    if arguments.recursive != None:
        rFactor = arguments.recursive
        if rFactor > 0 and rFactor <= 4:
            info["recursive"] = (True, rFactor)
        else:
            info["recursive"] = (False,-1)
    else:
        info["recursive"] = (False, -2)


    if arguments.optimize and info["recursive"][1] < 1:
        printError("The optimize tag is only useful if you set a recursivity factor greater than 1")
    elif (not arguments.optimize) and info["recursive"][1] > 1:
        printWarning("You have set the recursive option without setting the optimize flag.")
        printWarning("The time taken by the algorithm will be set to the power of %s" % rFactor)
    info["optimize"] = (True, arguments.optimize)

    if arguments.thread != None:
        info["thread"] = (True,arguments.thread)
    else:
        info["thread"] = (False,0)

    return (is_valid,info)


def isAValidDommainName(pDomains):
    r = search(lookLikeDomainRegex, str(pDomains))
    if r == None:
        return False, "No domains"
    domain = r.group()
    if "www." in domain:
        domain = domain[4:]
    return True, domain

def isAValidWorlList(wlPath):
    if exists(wlPath):
        try:
            possible_subdomains = open(wordlist_path,'r')
            return (True, possible_subdomains)
        except:
            return (False, "Can't open wordlist file")
    else:
        return (False, "File : " + str(arguments.wordlist)+" does not exists")

def init(infos):
    d = infos["domain"][1]
    w = "subdomains.txt"
    r = 1
    t = 10

    isWl, wl_Path = infos["wordlist"]
    if not isWl:
        if wl_Path != "":
            printError(wl_path)
        printWarning("Default wordlist : subdomains.txt")
    else:
        w = wl_Path

    isR, rLvl = infos["recursive"]
    if not isR:
        if rLvl == -1:
            printError("Recursive number too high")
        printWarning("default recursor level : 1")
    else:
        r = rLvl

    isT, tLevel = infos["thread"]
    if not isT:
        if tLevel == -2:
            printError("Thread number too low")
        printWarning("default thread level : 10")
    else:
        t = tLevel

    printInit(d,t,w,r,infos["optimize"][1])
    return d,w,r,t, infos["optimize"][1]
