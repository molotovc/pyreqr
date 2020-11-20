# pyreqr
Distributed threaded python Requests testing tool

Requires
- pip installed requests and fake_useragent

Usage
- Run the script
- With prefilled setup: py(thon3) pyreqr.py -r -s -d www.domain.com -t 250

Parameters
- --reckless, --ssl, --http, --domain x, --port 0, --threads 1
- -d can be domainame or IPv4 address -p optional and required with IPv4

Text files
- proxyhttp for all http proxies
- proxyhttps for all https proxies
- proxyhttpr for bulk unsure proxies http(s)

SSL/HTTPS Requests to an IPv4 address is not recommended as it should throw an SSLError by default.
Caution! Tool as is might send all requests coming from your default gateway. (see proxyhttp* files)
Fill proxies in their .txt file 1 address:port each line no spaces and no empty lines.
