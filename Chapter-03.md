#  第三天
## 线程
线程是中轻量级的进程，所有线程均在同一个进程中，共享全局内存，用于任务并行
###  通过函数使用线程
实例1
````buildoutcfg
import threading
import time


def helloworld():
    time.sleep(2)
    print("helloworld")


t = threading.Thread(target=helloworld)
t.start()
print("main thread")

````
注意：这里有两个线程一个是主线程，一个是通过threading模块产生的t线程，
这里程序并没有阻塞在helloword函数，主线程和t线程并行运行


实例2 同种任务并行

````buildoutcfg
import threading
import time


def helloworld(id):
    time.sleep(2)
    print("thread %d helloworld" % id)


for i in range(5):
    t = threading.Thread(target=helloworld, args=(i,))
    t.start()
print("main thread")
````

实例3 线程间同步

````buildoutcfg
import threading, time

count = 0

def adder():
    global count
    count = count + 1
    time.sleep(0.5)
    count = count + 1

threads = []
for i in range(10):
    thread = threading.Thread(target=adder)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(count)
````

加锁
````buildoutcfg
import threading, time

count = 0

def adder(addlock):
    global count
    addlock.acquire()
    count = count + 1
    addlock.release()
    time.sleep(0.1)
    addlock.acquire()
    count = count + 1
    addlock.release()

addlock = threading.Lock()
threads = []
for i in range(100):
    thread = threading.Thread(target=adder,args=(addlock,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(count)
````
使用with 加锁

````buildoutcfg
import threading, time

count = 0

def adder(addlock):
    global count
    with addlock:
        count = count + 1
    time.sleep(0.1)
    with addlock:
        count = count + 1

addlock = threading.Lock()
threads = []
for i in range(100):
    thread = threading.Thread(target=adder,args=(addlock,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(count)
````

### 通过类使用线程

实例1
继承threading.Thread 重写run方法
````buildoutcfg
import threading, time


class HelloWorld(threading.Thread):
    def run(self):
        time.sleep(2)
        print("hellowrold")


t = HelloWorld()
t.start()
print("main thread")
````

实例2
````buildoutcfg
import threading, time


class HelloWorld(threading.Thread):
    def __init__(self, id):
        self.id = id
        super(HelloWorld, self).__init__()
    def run(self):
        time.sleep(2)
        print("thread %d hellowrold" % self.id)

for i in range(5):
    t = HelloWorld(i)
    t.start()
print("main thread")
````

实例3
````buildoutcfg
import threading, time


class HelloWorld(threading.Thread):
    count = 0
    def run(self):
        HelloWorld.count += 1
        time.sleep(0.5)
        HelloWorld.count += 1

threads = []
for i in range(5):
    t = HelloWorld()
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(HelloWorld.count)
````

加锁
````buildoutcfg
import threading, time


class HelloWorld(threading.Thread):
    count = 0
    addlock = threading.Lock()
    def run(self):
        with HelloWorld.addlock:
            HelloWorld.count += 1
        time.sleep(0.5)
        with HelloWorld.addlock:
            HelloWorld.count += 1

threads = []
for i in range(5):
    t = HelloWorld()
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(HelloWorld.count)
````

### queue 模块

实际上带有线程的程序通常由一系列生产者和消费者组成，它们通过将数据存入一个共享队列中或者从中取出来进行通信。

````buildoutcfg
import threading, queue
import time


numconsumers = 20
numproducers = 20
nummessages = 4

lock = threading.Lock()
dataQueue = queue.Queue()


def producer(idnum):
    for msgnum in range(nummessages):
        dataQueue.put("producer id=%d, count=%d" % (idnum, msgnum))


def consumer(idnum):
    while True:
        data = dataQueue.get()
        with lock:
            print("consumer", idnum, "got => ", data)
        time.sleep(0.1)
        dataQueue.task_done()

if __name__ == "__main__":
    consumerThreads = []
    producerThreads = []
    for i in  range(numproducers):
        t = threading.Thread(target=producer, args=(i,))
        producerThreads.append(t)
        t.start()
    for i in range(numconsumers):
        t = threading.Thread(target=consumer, args=(i,))
        t.daemon=True
        consumerThreads.append(t)
        t.start()

    dataQueue.join()
````

类
````buildoutcfg
import threading, queue
import time


numconsumers = 2
numproducers = 2
nummessages = 4

dataQueue = queue.Queue()


class Producer(threading.Thread):
    def __init__(self, idnum, nummessages):
        self.idnum = idnum
        self.nummessages = nummessages
        super(Producer, self).__init__()


    def run(self):
        for msgnum in range(self.nummessages):
            dataQueue.put("producer id=%d, count=%d" % (self.idnum, msgnum))


class Consumer(threading.Thread):
    lock = threading.Lock()
    def __init__(self, idnum):
        self.idnum = idnum
        super(Consumer, self).__init__()

    def run(self):
        while not dataQueue.empty():
            data = dataQueue.get(block=False)
            with Consumer.lock:
                print("consumer", self.idnum, "got => ", data)
            time.sleep(0.1)

if __name__ == "__main__":
    consumerThreads = []
    producerThreads = []
    for i in  range(numproducers):
        t = Producer(i, nummessages)
        producerThreads.append(t)
        t.start()
    for i in range(numconsumers):
        t = Consumer(i)
        consumerThreads.append(t)
        t.start()
    for t in producerThreads:
        t.join()
    for t in consumerThreads:
        t.join()
````
练习: 使用多线程写一个并发http，get请求的程序，
可设置并发数和请求总数，返回请求状态码
## 多进程
###  multiprocessing  模块
多进程模块
````buildoutcfg
import os

from multiprocessing import Process, Lock

def whoami(label, lock):
    msg = '%s: name:%s, pid:%s'
    with lock:
        print(msg % (label, __name__,os.getpid()))


if __name__ == '__main__':
    lock = Lock()

    for i in range(5):
        p = Process(target=whoami, args=('child', lock))
        p.start()
````


队列和子类

````buildoutcfg
import time, queue
from multiprocessing import Process, Queue, Lock


class Consumer(Process):
    lock = Lock()
    def __init__(self, id, q):
        self.id = id
        self.post = q
        super(Consumer,self).__init__()

    def run(self):
        while True:
            try:
                data = self.post.get(block=False)
            except queue.Empty:
                break
            with Consumer.lock:
                print("process id: %d,data:%d" % (self.id, data))
            time.sleep(0.1)

if __name__ == '__main__':
    q = Queue()
    for i in range(10):
        q.put(i)

    for i in range(2):
        c = Consumer(i, q)
        c.start()
````
进程池
```
from multiprocessing import Pool
import time

def func(num):
    print("hello world %d" % num)
    time.sleep(3)
    

if __name__ == '__main__':
   
    pool = Pool(processes=4)
    
    for i in range(100):
        pool.apply_async(func, (i,))
    pool.close()
    pool.join()
    

```
pool.map

```
from multiprocessing import Pool
import time
def f(x):
    time.sleep(0.5)
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, range(10)))
```

##   协程
协程，又成为微线程
###  yield
````buildoutcfg
def helloWorld(n):
    while True:
        p = yield
        print("hello world %d: %d" % (n, p) )

g1 = helloWorld(1)
g2 = helloWorld(2)
g3 = helloWorld(3)

next(g1)
next(g2)
next(g3)
for i in range(5):
    g1.send(i)
    g2.send(i)
    g3.send(i)
````

分段累加
````buildoutcfg
def addnum(start, end):
    sum = 0
    for i in range(start, end):
        sum += i
        # print(sum)
        yield
    return sum


g1 = addnum(1,51)
g2 = addnum(51,101)

next(g1)
next(g2)
for i in range(50):
    try:
        g1.send(1)
    except StopIteration as exc:
        sum1 = exc.value
    try:
        g2.send(1)
    except StopIteration as exc:
        sum2 = exc.value
print(sum1 + sum2)
````

### asyncio

````buildoutcfg
import asyncio

async def hello_world():
    print("Hello World!")

loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())
loop.close()
````

分段累加
````buildoutcfg
import asyncio
async def addnum(start, end):
    sum = 0
    for i in range(start, end):
        sum += i
    return sum


loop = asyncio.get_event_loop()
s1 = loop.run_until_complete(addnum(1,51))
s2 = loop.run_until_complete(addnum(51,101))
loop.close()
print(s1+s2)
````
##作业
使用多进程写一个并发http，get请求的程序， 可设置并发数和请求总数，返回请求状态码
