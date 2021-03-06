# pyreqr
Distributed threaded python GET Requests stress testing tool

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

Caution! Proxyhttp files might send all requests originating from your default gateway / router. (see proxyhttp* files)
SSL/HTTPS Requests to an IPv4 address is not recommended as it should throw an SSLError by default. Fill proxies in their .txt file 1 address:port each line no spaces and no empty lines.

Performance, bottlenecks and more information
- CPU, (LAN/)WAN & Proxy bandwidth / throughput (networking speed) dependent (Higher = better)
- Machine - network - proxy - endpoint latency (Lower = better)
- Amount of data transfered each request (Higher = most destructive and lowers requests/s & Lower = least destructive and increases requests/s)
- Endpoint load capabilities (Lower is better for achieving a 503 Service unavailable error)

Tool should be able to generate up to a 100 requests/s on moderate hardware with decent proxies. Starting from a 100 threads you can work your way up until the requests/s don't improve anymore. Tested on Intel® Core™ i7-7500U CPU @ 2.70GHz × 4 (1 core used) achieves ~250 requests/s. On the same machine tested i've easily executed up to 5000 threads but the requests/s would stay arround 250. (my max performance)

Caution! Do not remove any sleep command present in this program to try and improve performance increase threads instead till you've reached your machine's max. performance. (requests/s won't go higher) Removing sleep commands in this program will mess up threading computations and could harm the hardware of your machine due to several endless loops. The sleep command simply leaves room for the next thread in line to do it's work and so on.. As a testing tool this program does not include multiprocessing capabilities. It can however be easily replicated using multiple command line interfaces running the same tool.

More powerful tools alike can most likely be found in C++ language appliances as interpreted languages like python have interpreting bottlenecks that do slow down computing tasks in bare comparison to compiled languages.
