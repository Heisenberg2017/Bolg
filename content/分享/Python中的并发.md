---
title: "Python中的并发"
date: 2019-11-29T13:56:35+08:00
draft: false
---
介绍Python中的并发(文章中出现的代码文件源码在最末尾)
<!--more-->

## 斐波那契数列
```
+------------------------------------------+
|             Fibonacci数列                 |
|------------------------------------------|
| 斐波那契数列指的是这样一个数列              |
| 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...    |
|                                          |
| 这个数列从第3项开始，每一项都等于前两项之和  |
|  2 = 1 + 1                               |
|  3 = 2 + 1                               |
|  5 = 3 + 2                               |
|  8 = 5 + 3                               |
| 13 = 8 + 5                               |
| ...                                      |
+------------------------------------------+
```
什么是I/O密集和CPU密集?

CPU密集型也叫计算密集型，指的是系统的硬盘、内存负载相对CPU要低很多，此时，系统运作大部分的状况是CPU Loading 100%，CPU要读/写I/O(硬盘/内存)，I/O在很短的时间就可以完成，而CPU还有许多运算要处理，CPU 负载很高。

IO密集型指的是系统的CPU性能相对硬盘、内存负载要低很多，此时，系统运作，大部分的状况是CPU在等I/O (硬盘/内存/网络) 的读/写操作，此时CPU 负载并不高。

下面是实现的一个函数，我们准备使用这个函数提供web服务，通过调整n的值来模拟CPU密集和IO密集的情况，这个例子中n越高则CPU负载越高

```python
# fib.py
def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
```
  

## 单线程

什么是单线程?

是操作系统能夠進行運算调度的最小單位。
大部分情况下，它被包含在进程之中，是进程中的實際運作單位。
一条线程指的是进程中一个单一顺序的控制流，一個进程中可以並行多個线程，每条线程并行执行不同的任务。



单线程有没有什么问题或者缺陷？

对外提供web服务，使用单线程的程序只能对一个在线用户进行服务



验证

1.实现一个对外提供计算斐波那契额数的单线程服务

这里我们已经实现好了直接python one_server.py运行就可以对外提供服务

2.先使用 nc 连接上去，看下是否能够正常计算斐波那契, 然后使用第二个 nc 客户端连接上去，看下是否可以正常对外提供服务

![单进程服务器](/images/单进程服务器.png "单进程服务器")


3.测试性能

python perf2.py 25000 25000 1 双客户端的情况
![单线程IO密集情况下双客户端性能](/images/单线程IO密集情况下双客户端性能.png "单线程IO密集情况下双客户端性能")
python perf2.py 25000 25000 20 双客户端的情况
![单线程CPU密集情况下双客户端性能](/images/单线程CPU密集情况下双客户端性能.png "单线程CPU密集情况下双客户端性能")




<!--
开始演示单线程
    0.fib适合模拟cpu密集的情况
    1.现在我还需要模拟一个i/o密集的情况用作对照
    3.i/o包括读写磁盘，网络传输
    4.我这里用网络传输来模拟io
    5.所以 我现在准备对外提供这个计算fib的微服务
    6.开始操作
    7.一个客户端IO密集
    8.开始提问，你们知道单线程情况下第二个客户端上来会怎么样吗?
    9.第二个客户端链接，没有任何回应
    10.上面使用nc
    10.上图
    11.讲讲为什么没有回应
    12.最后做下性能测试
-->

运行时草图
```
+----------------------------+
|  Process                   |                  +-----------+
|              main thread   |        send      |           |
|             +----------+   |  <-------------+ |           |
|             |   recv   |   |                  |  client1  |
|             |    |     |   |  +-------------> |           |
|             |   fib(n) |   |        resp      |           |
|             |    |     |   |                  +-----------+
|             |   send   |   |
|             +----------+   |
|                            |      connect     +-----------+
|             +----------+   |  <-------------+ |           |
|             |  accept  |   |                  |  client2  |
|             +----------+   |      无 响 应     |           |
+----------------------------+                  +-----------+
```

这个例子中的单线程遵守下面的原则

原则:

 * 谁先来为谁服务

 * 上一个走了才能为下一个人服务
 
<!--
我们如何让它服务多个客户端，任何服务都是需要服务多客户端的
    1.类比生活中的例子
    0.单线程同一个时间只能对一个人服务,所以我们需要多线程
    2.开始一顿操作
    3.先使用nc 让大家看到可以两个同时连接上去
    4.多线程
    5.开始性能测试
    6.第二个客户端链接上之前提问大家，性能会有什么变化
    6.对比I/O密集 CPU密集情况下处理第二个客户端的性能变化
    7.引出GIL
-->



## 多线程

为什么要有多线程?


因为单线程无法处理多个用户同时访问web服务的情况


多线程有没有什么问题或者缺陷？


有GIL导致无法使用多核核心


验证

1.实现一个对提供计算斐波那契额数的多线程服务

这里我们已经实现好了直接python thread_server.py运行就可以对外提供服务

2.使用 nc 连接上去，看下对外提供服务的情况,这里关注两个nc连接上去是否都会有应答

测试性能 
python perf2.py 25000 1

![多线程IO密集情况下双客户端](/images/多线程IO密集情况下双客户端.png "多线程IO密集情况下双客户端")

I/O密集情况下

 * 可以同时服务多个客户端
 * 多线程可以提升处理请求总量

测试性能 python perf2.py 25000 20
![多线程CPU密集情况下双客户端](/images/多线程CPU密集情况下双客户端.png "多线程CPU密集情况下双客户端")


CPU密集情况下

 * 可以同时服务多个客户端
 * 新增客户端服务器可以处理的总量基本不变
 * 确实无法利用多核
 
这个会产生一个现象,就是一个人计算一次fib可能需要10s,这个时候第二个人登陆上来了，这样每个人计算的时间就要20s，3个人就30s,以此类推
这里可以使用开启两个python perf1.py 25000 25 来验证

运行时草图
```python
+----------------------------------------+
|  Process                   thread1     |                  +-----------+
|                          +----------+  |        send      |           |
|                          |   recv   |  |  <-------------+ |           |
|                          |    +     |  |                  |  client1  |
|                   +--------->fib(n) |  |  +-------------> |           |
|                   |      |    +     |  |        resp      |           |
|    +-------+      |      |   send   |  |                  +-----------+
|    |       |      |      +----------+  |
|    |  GIL  +------+                    |
|    |       |      |         thread2    |                  +-----------+
|    +-------+      |      +----------+  |        send      |           |
|                   |      |   recv   |  |  <-------------+ |           |
|                   |      |    +     |  |                  |  client1  |
|                   ---------->fib(n) |  |  +-------------> |           |
|                          |    +     |  |        resp      |           |
|                          |   send   |  |                  +-----------+
|                          +----------+  |
|                                        |
|                                        |
|                           main thread  |      connect     +-----------+
|                          +----------+  |  <-------------+ |           |
|                          |  accept  |  |                  |  client2  |
|                          +----------+  |  +-------------> |           |
+----------------------------------------+        resp      +-----------+
```



## GIL
![Python多线程](/images/Python多线程.gif "Python多线程")

为什么会有GIL?


因为Python的内存管理不是线程安全的
啥是线程安全，这个后面讲，在引出Python的内存管理之后
python多线程是鸡肋，由于GIL的存在只能利用一个CPU? 
实际上GIL是Cpython的



Python如何进行内存管理?



引用计数为主，标记-清除和分代收集两种机制




## 内存管理
问题: 学校有一些办公场所用于租给各个部门协会，办公场所是有限的，你会如何管理这些场地的分配和回收？

以下是条件

 * 每个协会/部门及任何人都可以租用场地
 * 允许共用一块场地
 * 当一个场地没有任何人使用时需要进行回收，然后等待其他部门申请用于其他的用途



几个方案

0.直接申请，不要的时候再告诉学校，如果你忘记了，这块空间就一直处于不可以用的情况

1.定时询问，比如每周五询问一次有没有人使用，全部统计结束前的时候不允许分配场地，避免出现刚才统计结果不一致
这种方法需要停止所有场地的分配，还要询问等待所有人回复

2.引用计数，竞争，因为分配和增加引用时很频繁的，频繁的锁解锁十分的影响性能

3.拥有权，部门协会申请后在某个区间范围内可以使用这片区域，例如有个活动开始申请，活动结束立马就回收

。。。。。。




## 多进程

为什么要有多进程?


存在GIL使得Python多线程无法利用多个核心


多进程有没有什么问题或者缺陷？

fork系统调用太慢，multiprocess由于引用计数还导致了Python用不了linux写时复制的功能,
耗费内存太多


验证

1.实现一个对提供计算斐波那契额数的有多进程服务

这里我们已经实现好了直接python multiprocess_server.py运行就可以对外提供服务


2.测试性能 

python perf2.py 25000 1
![多进程IO密集情况下双客户端](/images/多进程IO密集情况下双客户端.png "多进程IO密集情况下双客户端")
I/O密集情况下 
 
 * 多进程相对多线程性能下降非常多
 * 新增客户端服务器可以处理的总量有提升
 
python perf2.py 25000 20
 ![多进程CPU密集情况下双客户端](/images/多进程CPU密集情况下双客户端.png "多进程CPU密集情况下双客户端")
CPU密集情况下 

 * 单个可处理总量略有下降
 * 新增客户端服务器可以处理的总量提升明显

运行时草图

```
+---------------------+       +----------------------------------------+
    Process Pool      |       | Process                                |
                      |       |                                        |
      +-----------+   |       |                            thread1     |
      |Process1   |   |       |                          +----------+  |
      |   +-----+ |   |       |                          |   recv   |  |
      |   | GIL | |   |       |   fib任务提交给进程池处理  |    +     |  |
      |   +-----+ |   |  <--------------------------------+ submit  |  |
      +-----------+   |       |       计算完成返回结果     |    +     |  |
                      |  +--------------------------------> result  |  |
      +-----------+   |       |                          |    +     |  |
      |Process2   |   |       |                          |   send   |  |
      |   +-----+ |   |       |                          +----------+  |
      |   | GIL | |   |       |                                        |
      |   +-----+ |   |       |                            thread2     |
      +-----------+   |       |                          +----------+  |
                      |       |                          |   recv   |  |
      +-----------+   |       |   fib任务提交给进程池处理  |    +     |  |
      |Process3   |   |  <--------------------------------+ submit  |  |
      |   +-----+ |   |       |       计算完成返回结果     |    +     |  |
      |   | GIL | |   |  +--------------------------------> result  |  |
      |   +-----+ |   |       |                          |    +     |  |
      +-----------+   |       |                          |   send   |  |
                      |       |   +-------+              +----------+  |
            X         |       |   |       |                            |
                      |       |   |  GIL  |其 余 部 分 同 多 线 程 版 本 |
            X         |       |   |       |                            |
                      |       |   +-------+                            |
            X         |       |                                        |
 +--------------------+       +----------------------------------------+


```







## 协程

为什么要有协程?


为什么一个线程只能为一个客户服务，对比现实世界，
一个人只能为一个客户服务，这样太浪费了，为什么不能一个人，同时为多人服务？


协程有没有什么问题或者缺陷？



协程在I/O密集情况下可以发挥最大的作用，如果时CPU密集会导致协程阻塞,这个时候仍需要使用multiprocess


验证


1.这里我们已经实现好了直接aserver.py运行就可以对外提供服务


 ![协程CPU密集时阻塞](/images/协程CPU密集时阻塞.png "协程CPU密集时阻塞")

* 协程的现象和线程相似，不过性能稍微低一点(这点可以自己验证)
* 出现较长时间的计算任务使程序阻塞了

3.使用multiprocess解决阻塞的情况可以自己修改下代码去复现


运行时草图
```python
 Thread
   |
   |       +---------------+
   |       |               |
   |       |  代 码 块 A    |
   |       |               |
   |       |               |
   |       +---------------+
   |                                 +----------------+
时 |                                 |                |
   |                                 |   代 码 块 B    |
间 |                                 |                |
   |                                 +----------------+
   |
   |       +---------------+
   |       |  代 码 块 A    |
   |       +---------------+
   |                                 +----------------+
   |                                 |   代 码 块 B    |
   |                                 +----------------+
   |
   |
   v

```



## 大多数Web框架的方案


大多数的Python Web服务会采用下面的方式进行并发，而不是multiprocess

app1: python many_server.py 25000

app2: python many_server.py 25001


## 未来绕过GIL的方案
全局解释器锁是全局解释器状态的一部分。
 CPython 的进程可以有多个解释器，因此可以有多个锁，但是此功能很少使用，
 因为它只通过 C-API 公开。
 ![多解释器](/images/多解释器.png "多解释器")





## 性能测试
I/O 密集情况下:

这里假定n=1时为i/o密集型
这里假定n=20时为cpu密集型
适当的调高n可以让对比结果更加明显


代码    | 1个客户端    | 2个客户端
:---- | :---- | :----
one_server | 12 000 reqs/sec | 无法对外提供服务
thread_server |  12 000 reqs/sec  |  19 000 reqs/sec
multiprocess_server |  3 500  reqs/sec  |  4 300 reqs/sec
many_server |  12 000  reqs/sec  |  20000 reqs/sec
go_server |  12 000 reqs/sec  |  20 000 reqs/sec
async_server | 8 000 reqs/sec  |  14 000 reqs/sec
subinterpreters_server &nbsp;&nbsp;&nbsp;&nbsp; | 4 000 reqs/sec &nbsp;&nbsp;&nbsp;&nbsp; |  5 000 reqs/sec

CPU 密集情况下:

代码    | 1个客户端    | 2个客户端
:---- | :---- | :----
one_server | 400    reqs/sec         |      无法对外提供服务
thread_serve | 400    reqs/sec         |        400 reqs/sec
multiprocess_server | 400    reqs/sec     |             700 reqs/sec
many_server  |  400 reqs/sec            |        800 reqs/sec
go_server   |  7 500    reqs/sec     |       11 000 reqs/sec
async_server     | 不再延伸             |     不再延伸
subinterpreters_server &nbsp;&nbsp;&nbsp;&nbsp; | 350reqs/sec &nbsp;&nbsp;&nbsp;&nbsp; |  350reqs/sec

 
   
## python vs golang

聊一聊国内很多大厂迁移到go的事情

国内很多大厂迁移到go或者重度使用go,性能，不能利用多核，太废内存
为此google甚至启动了一个疯狂的项目grumpy


## 总结
 * I/O密集型Python多线程和go的性能区别不大
 * CPU密集型go比Python快几十倍
 * Python多进程IO密集型性能比多线程差很多
 * CPU密集型情况下使用Python多进程会获得性能上的提升，多线程由于GIL性能不会提升，反而可能因为线程切换导致性能降低
 * Python协程可以替代多线程在IO密集场景下，且协程更轻量级，CPU密集情况下协程会阻塞，这个时候需要用到多进程
 * 未来解决GIL的方案是子解释器，比线程重，进程轻，但是在python3.8还没有开发完成,只是一种并行选择，并不能解决低效的问题

## 扩展阅读:
[CPU密集和I/O密集](https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean)
在stackoverflow上的解释

这次分享部分代码都来自David Beazley在PyCon2015的一场演讲
[Python Concurrency From the Ground Up: LIVE! - PyCon 2015](https://www.youtube.com/watch?v=MCs5OvhV9S4)
新版本Python代码的行为和演讲中已经不完全一样了，但仍然值得一看

讲讲啥是[GIL](http://cenalulu.github.io/python/gil-in-python/)

[GIL已死?](https://medium.com/hackernoon/has-the-python-gil-been-slain-9440d28fa93d)
答案是没死，讲了Python在新版本中可能用于绕过GIL的方案

如何阅读CPYTHON [cpython-source-code-guide](https://realpython.com/cpython-source-code-guide/)

youtube前端大量使用Python，在各种优化方案都渐渐失去效果时，鬼魅想法涌上心头
[google疯狂的项目](https://github.com/google/grumpy)

InfoQ 说说 [grumpy](https://www.infoq.cn/article/2017/01/Grumpy-Google-Go-Python) 也就是上面说的疯狂的项目

Python引用计数导致多进程无法利用写时复制,Python优化文章大厂Instagram出品
[译文](https://learnku.com/python/t/22973/instagram-actual-combat-exploring-write-time-replication-friendly-python-garbage-collection-mechanism)
[原文](https://instagram-engineering.com/dismissing-python-garbage-collection-at-instagram-4dca40b29172)


## 源码文件
单线程版本
python one_server.py 直接运行
```python
# python3
# one_server.py
import sys
from socket import *
from fib import fib


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        fib_handler(client)


def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed")


fib_server(('', 25000))

```

多线程版本
python thread_server.py 直接运行
```python
# thread_server.py
# python3
# server.py
# Fib microservice
# Use Python 3

from socket import *
from fib import fib
from threading import Thread


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        task = Thread(target=fib_handler, args=(client,))
        task.daemon = True
        task.start()


def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed")


fib_server(('', 25000))

```

多进程版本
python multiprocess_server.py 直接运行
```python
# multiprocess_server.py
# server.py
# Fib microservice
# Use Python 3

from socket import *
from fib import fib
from threading import Thread
from multiprocessing import Pool
# from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)



def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        task = Thread(target=fib_handler, args=(client,))
        task.daemon = True
        task.start()


def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        future = pool.apply(fib, (n,))
        resp = str(future).encode('ascii') + b'\n'
        client.send(resp)
    print("Closed")


fib_server(('', 25000))

```

协程版本
python aserver.py 直接运行
```python
# aserver.py
# python3

from socket import *
from fib import fib
from collections import deque
from select import select
from concurrent.futures import ThreadPoolExecutor as Pool
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)

tasks = deque()
recv_wait = {}  # Mapping sockets -> tasks (generators)
send_wait = {}
future_wait = {}

future_notify, future_event = socketpair()


def future_done(future):
    tasks.append(future_wait.pop(future))
    future_notify.send(b'x')


def future_monitor():
    while True:
        yield 'recv', future_event
        future_event.recv(100)


tasks.append(future_monitor())


def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # No active tasks to run
            # wait for I/O
            can_recv, can_send, _ = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))

        task = tasks.popleft()
        try:
            why, what = next(task)  # Run to the yield
            if why == 'recv':
                # Must go wait somewhere
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            elif why == 'future':
                future_wait[what] = task
                what.add_done_callback(future_done)

            else:
                raise RuntimeError("ARG!")
        except StopIteration:
            print("task done")


class AsyncSocket(object):
    def __init__(self, sock):
        self.sock = sock

    def recv(self, maxsize):
        yield 'recv', self.sock
        return self.sock.recv(maxsize)

    def send(self, data):
        yield 'send', self.sock
        return self.sock.send(data)

    def accept(self):
        yield 'recv', self.sock
        client, addr = self.sock.accept()
        return AsyncSocket(client), addr

    def __getattr__(self, name):
        return getattr(self.sock, name)


def fib_server(address):
    sock = AsyncSocket(socket(AF_INET, SOCK_STREAM))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = yield from sock.accept()  # blocking
        print("Connection", addr)
        tasks.append(fib_handler(client))


def fib_handler(client):
    while True:
        req = yield from client.recv(100)  # blocking
        if not req:
            break
        n = int(req)

        # solve block issue
        # future = pool.submit(fib, n)
        # yield 'future', future
        # result = future.result()    #  Blocks

        result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        yield from client.send(resp)  # blocking
    print("Closed")


tasks.append(fib_server(('', 25000)))
run()

```

子解释器版本(社区开发中)
python subinterpreters_server.py 直接运行
```python
# python3.8
# subinterpreters_server.py

import _xxsubinterpreters as interpreters
from socket import *
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool
import textwrap as tw
import marshal

pool = Pool(4)


def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        interpid = interpreters.create()

        # Create a channel
        channel_id = interpreters.channel_create()

        # Pre-populate the interpreter with a module
        interpreters.run_string(interpid,
                                "import marshal; import _xxsubinterpreters as interpreters")

        # inp = marshal.dumps(client)
        # interpreters.channel_send(channel_id, inp)

        Thread(target=fib_handler, args=(interpid, channel_id, client), daemon=True).start()


def fib_handler(interpid, channel_id, client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)

        # print(n)
        interpreters.run_string(interpid,
                                tw.dedent("""
def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


result = fib(n)
# print('r', result)
result_raw = marshal.dumps(result)
interpreters.channel_send(channel_id, result_raw)
                """),
                                shared=dict(
                                    channel_id=channel_id,
                                    n=n

                                ),
                                )
        result = None
        while not result:
            try:
                result = interpreters.channel_recv(channel_id)
            except Exception as e:
                pass
        resp = marshal.loads(result)
        resp = str(resp).encode('ascii') + b'\n'
        client.send(resp)


if __name__ == '__main__':
    fib_server(('', 25000))

```

处理时间
python perf1.py 25000(监听的端口) 1(fib函数中的n)
```python
# python3
# perf1.py

from socket import *
import time
import sys

port, x = sys.argv[1:]

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', int(port)))

while True:
    start = time.time()
    sock.send((x + '\n').encode())
    resp =sock.recv(100)
    end = time.time()
    print(end-start, resp)

    

```

处理次数
python perf2.py 25000(监听的端口) 1(fib函数中的n)
```python
# python3
# perf2.py
# requests/sec of fast requests

from socket import *
from threading import Thread
import time
import sys

port, x = sys.argv[1:]

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', int(port)))

n = 0


def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0


task = Thread(target=monitor)
task.daemon = True
task.start()

while True:
    sock.send((x + '\n').encode())
    resp =sock.recv(100)
    n += 1

```

go run server.go 运行 注意go监听的是5000
```go
// server.go
package main

import (
    "fmt"
    "net"
    "strconv"
)

func fibonacci(num int) int{
	if num<=2{
		return 1
	}

	return fibonacci(num-1) + fibonacci(num-2)
}

func main() {
    fmt.Println("Starting the server ...")
    // 创建 listener
    listener, err := net.Listen("tcp", "localhost:50000")
    if err != nil {
        fmt.Println("Error listening", err.Error())
        return //终止程序
    }
    // 监听并接受来自客户端的连接
    for {
        conn, err := listener.Accept()
        if err != nil {
            fmt.Println("Error accepting", err.Error())
            return // 终止程序
        }
        go doServerStuff(conn)
    }
}

func doServerStuff(conn net.Conn) {
    for {
        buf := make([]byte, 512)
        len, err := conn.Read(buf)
        if err != nil {
            fmt.Println("Error reading", err.Error())
            return //终止程序
        }
        n, _ := strconv.Atoi(string(buf[:len-1]))
        // fmt.Println(string(buf[:len-1]))
        // fmt.Println(n, err)
        ret := fibonacci(n)
        // ifmt.Println(n)
        // fmt.Println(ret)
        data := strconv.Itoa(ret)
        // fmt.Println(data)
        conn.Write([]byte(data + "\n"))
    }
}
```