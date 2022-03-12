import dns.name
import dns.message
import dns.query
import dns.flags
from urllib3 import PoolManager

GOOGLE_DNS = "8.8.8.8"
ADDITIONAL_RDCLASS = 65535
HTTP_REQUESTER = PoolManager()
HEADERS =   { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def testGoogleDNS(domain):
    return makeDNSquery(GOOGLE_DNS,domain)

def makeDNSquery(dns_ip,domain):
    request = dns.message.make_query(domain, dns.rdatatype.ANY)
    request.flags |= dns.flags.AD
    request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS,dns.rdatatype.OPT, create=True, force_unique=True)
    response = dns.query.tcp(request, dns_ip)
    ip_address = response.answer
    all_ip = []
    if len(ip_address) > 0:
        for id_ in range(len(ip_address)):
            for ip_id in range(len(ip_address[id_])):
                ip = str(ip_address[id_][ip_id]).split(' ')[-1]
                all_ip.append(ip)
        return (True , all_ip)
    return (False , all_ip)

def testSubdomains(domain):
    hasrecord,ips = testGoogleDNS(domain)
    if hasrecord:
        try:
            response = HTTP_REQUESTER.request("GET", "https://"+domain+"/", timeout=5)
            return (True, response.status)
        except:
            return (True, -2)

    return (False, -1)
