# coding=utf-8
import socket,time,threading,Queue
from bs4 import BeautifulSoup

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

q = Queue.Queue(maxsize=20)


def http_url(*list2):
	q.put(1)
	url,p,ip = list2;
	str2 = '''GET / HTTP/1.1
Host: %s
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Accept-Language: zh-CN,zh;q=0.8

'''% (url)
	try:
		s.connect( ( '%s'  % (ip) ,p )    )
		s.sendall(str2) 
		html=s.recv(3048)
	except Exception,e:
		#print Exception,e;
		q.get()
		return False;
	soup = BeautifulSoup(html,"html.parser")
	title = soup.title.string;
	print "URL:%s --> IP: %s  ------> Title: %s" % (url,ip,title)
	q.get()
	time.sleep(0.5)


file_ip = open('./ip.txt','r')
for ip in file_ip:
	ip = ip.replace("\r","").replace("\n","");
	while True:
		if not q.full():
			t = threading.Thread(target=http_url,args=['src2.cc',80,ip]); 
			t.start();
			break;
		else:
			time.sleep(1)
file_ip.close()

