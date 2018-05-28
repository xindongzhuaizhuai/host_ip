# coding=utf-8
import socket,time,threading,Queue,sys,requests
from base64 import b64encode;
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')


q = Queue.Queue(20)


def http_url(*list2):
	q.put(1)
	url,p,ip = list2;
	str2 = '''GET / HTTP/1.1
Host: %s
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Accept-Language: zh-CN,zh;q=0.8


'''% (url)
	str3 = '''GET / HTTP/1.1
Host: %s
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Accept-Language: zh-CN,zh;q=0.8


'''% (str(ip))
	try:
		html = "123";
		socket.setdefaulttimeout(10)
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect( ( '%s'  % (ip) ,p )    )
		s.sendall(str2) 
		html=s.recv(3048);
	except Exception,e:
		print url,"--->",ip,"No"
		# print e;
		#print Exception,e;
		q.get()
		return False;
	soup = BeautifulSoup(html,"html.parser")
	try:
		title = soup.title.string;
	except Exception,e:
		title = b64encode(html);
	if title != 'Service Unavailable' and title != '403 Forbidden':
		try:
			html1 = "123";
			# r1 = requests.get('http://%s/'% str(ip),timeout=20); 
			# html1 = r1.text; 
			s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s1.connect( ( '%s'  % (ip) ,p )  );
			s1.sendall(str3) 
			html1=s1.recv(3048);
			soup1 = BeautifulSoup(html1,"html.parser")
			title1 = soup1.title.string;
		except Exception,e:
			title1 = b64encode(html1);
		try:
			html2 = "123";
			s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s2.connect( ( '%s'  % (ip) ,p )  );
			s2.sendall(str3) 
			html2=s2.recv(3048);
			soup2 = BeautifulSoup(html1,"html.parser")
			title2 = soup2.title.string;
		except Exception,e:
			title2 = b64encode(html2);

		if (title1 != title) and (title1 != title2) and (title1 != '403 Forbidden'):
			text =  "URL:%s --> IP: %s  ------> Title: %s  " % (url,ip,title)
			print text
			f = open('test.txt', 'a');
			f.write(text+"\r\n");
			f.close()
	else:
		print url,"--->",ip,"No"
	q.get()
	time.sleep(0.5)


file_ip = open('./ip.txt','r')
file_host = open('./host.txt','r')

for host in file_host:
	print host,"--->"
	for ip in file_ip:
		if ip.count("*") == 1:
			for ip_x in xrange(1,255):
				ip2 = ip.replace("*",str(ip_x));
				while True:
					if not q.full():
						t = threading.Thread(target=http_url,args=[host,80,ip2]); 
						t.start();
						break;
					else:
						time.sleep(1)
				time.sleep(0.5)
		elif ip.count("*") > 1:
			print "* buneng erge!"
			exit();
		else:
			while True:
				if not q.full():
					t = threading.Thread(target=http_url,args=[host,80,ip]); 
					t.start();
					break;
				else:
					time.sleep(1)

file_ip.close()
file_host.close()

