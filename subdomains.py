from argparse import ArgumentParser
from src.scan import initScan, getNbSubD, startScript
from src.testArgument import testAllArguments, scriptInit
from src.CLI import printBanner,printInfo, printError, printWarning
from src.testConnection import testSubdomains
import timeit

if __name__ == '__main__':
    parser = ArgumentParser(description="Description heres")
    parser.add_argument('-u', '--url', required=False, help="the url you want to test")
    parser.add_argument('-w', '--wordlist', required=False, help="")
    parser.add_argument('-r', '--recursive',type=int, required=False, help="")
    parser.add_argument('-t', '--thread',type=int, required=False, help="(int) The number of threads you wish to perform")
    parser.add_argument('--optimize',action='store_true', required=False)
    parser.add_argument('-c','--config', type=str, required=False)
    arguments = parser.parse_args()
    if arguments.url == None and arguments.config == None:
        printError("You need to use at least -u/--url flags or -c/--config")
        printWarning("You can also use -h or --help flag to have help")
        exit(1)

    printBanner()
    isOk, infos = testAllArguments(arguments)

    if not isOk:
        exit(1)
    printInfo("Script initialisation")
    d,w,r,t,o = scriptInit(infos)

    printInfo("Scan Initialisation")
    initScan(d,w,r,t,o)

    printInfo("Starting the script")
    start = timeit.default_timer()
    startScript()
    stop = timeit.default_timer()
    printInfo("There are %s subdomains for the links %s" % (getNbSubD(),d))
    printInfo("Compute duration : %s " % (stop - start))
