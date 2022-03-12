# Python Subdomains Scanning

## Explaination

Small tool developed in python 3.10.2 allowing to scan most of the subdomains of a website.
## Installation

```
git clone git@github.com:Sans-Atout/subdomains_scan_tool.git
cd subdomains_scan_tool/
pip install -r requirements.txt
```

## Run

```console
python subdomains.py -u url
```
### example : 

```console
python subdomains.py -u https://github.com/Sans-Atout/subdomains_scan_tool
```

## Arguments
* -u / --url : the domain you want to test
* -w / --wordlist : the subdomain wordlist you wish to test
* -t / --thread : the number of threads you wish to perform