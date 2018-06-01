#coding=utf-8
import requests,Queue,time,threading,socket,re,sys;
q = Queue.Queue(10);
reload(sys)
sys.setdefaultencoding('utf-8')

header1 = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}



def http(ip,p):
	q.put(1)
	url = "http://"+ip+":"+str(p).replace('\r','').replace('\n','');
	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sk.settimeout(3) #设置超时时间
	try:
		sk.connect((ip,p))
		#print 'kaifang'
	except Exception:
		#print 'bukaifang'
		q.get()
		sk.close()
		return 0
	sk.close()
	try:
		r = requests.get(url,timeout=15,verify=False,headers=header1);
		bianma =  r.encoding
		html = r.text.encode(bianma);
	except Exception,e:
		try:
			r = requests.get(url,timeout=15,verify=False,headers=header1);
			bianma =  r.encoding
			html = r.text.encode(bianma);
			#print Exception,e
		except Exception,e:
			q.get();
			return 0;
	title = re.findall("<title>[\s\S.]+</title>",html);
	if title:
		title = title[0].replace('\r','').replace('\n','');
	else:
		q.get();
		return 0;
	print url,"yes p:",p
	text = url+"---->title: %s " % (title);
	f = open('title.txt','a');
	f.write(text+"\r\n");
	f.close()
	q.get();



def q_Queue():
	while True:
		if not q.full():
			break;
		else:
			time.sleep(0.5)

p_p = [80,8080,88,8888]
for p in p_p:
	for ip in open('./ip.txt','r'):
		ip = ip.replace('\r','').replace('\n','');
		print "ip %s P: %i ============>" % (ip,p);
		if ip.count("*") >1 :
			exit();
		elif ip.count("*") == 1:
			for ip_x in xrange(1,255):
				ip2 = ip.replace("*",str(ip_x));
				q_Queue();
				print "ip %s P: %i qingqiu!! " % (ip2,p);
				t = threading.Thread(target=http,args=[ip2,p]);
				t.start()
		else:
			print "ip %s P: %i qingqiu!! " % (ip,p);
			t = threading.Thread(target=http,args=[ip,p]);
			t.start()


