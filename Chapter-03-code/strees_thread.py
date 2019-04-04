import threading, queue
import requests, time

start = time.time()

count = 100
num = 2
url = 'http://www.baidu.com'

lock = threading.Lock()
q = queue.Queue()
threads = []
result = {}


def get_content(url):
    while not q.empty():
        q.get(block=False)
        r = requests.get(url)
        with lock:
            try:
                result[r.status_code] = result.setdefault(r.status_code, 0) + 1
            except :
                result["error"] = result.setdefault("error", 0) + 1


for i in range(count):
    q.put(i)

for i in range(num):
    t = threading.Thread(target=get_content, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()
t = end - start
print("time %d" %  t)
for item in result:
    print("status_code[%s]: %d" % (item, result.get(item)))
