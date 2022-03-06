from argparse import ArgumentParser
from os.path import exists
from src.CLI import printBanner, printError, printInit, printResult, avancement, resetLine
from src.testConnection import testSubdomains

ADDITIONAL_RDCLASS = 65535
name_server = '8.8.8.8'

if __name__ == '__main__':
    parser = ArgumentParser(description="Description heres")
    parser.add_argument('-u', '--url', required=True, help="the url you want to test")
    parser.add_argument('-w', '--wordlist', required=False, help="")
    printBanner()

    arguments = parser.parse_args()
    testingDomain = str(arguments.url).split('/')[2]
    possible_subdomains = open('subdomains.txt','r').read().split('\n')
    wordlist_path = "subdomains.txt" 
    if arguments.wordlist != None:
        if exists(arguments.wordlist):
            wordlist_path = arguments.wordlist
            try:
                possible_subdomains = open(wordlist_path,'r').read().split('\n')
            except Exception as e: 
                print(e)
                exit(0)
        else: 
            printError("File : " + str(arguments.wordlist)+" does not exists")
            
    printInit(testingDomain,1, wordlist_path)
    print()
    nb_subDomains = 0
    _length = len(possible_subdomains) 
    for d_id in range(_length):
        d = possible_subdomains[d_id]
        url = d +"."+testingDomain
        avancement( (100 * (d_id+1)/_length), str(d_id) +'/'+str(_length))
        hasResult, status = testSubdomains(url)
        if hasResult:
            nb_subDomains = nb_subDomains + 1
            printResult(status, url)
    resetLine()
    print()
    print("There are %s subdomains for the links %s" % (nb_subDomains,testingDomain))