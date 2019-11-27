---
title: "Python进程、线程、协程"
date: 2019-11-05T11:09:29+08:00
draft: true
---
介绍一下这个文章说的啥巴拉巴拉的
<!--more-->

#### 斐波那契数列
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

<!--```python
# fib.py
def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
-->

<!--
开始演示斐波那契数列的特点
    0.为什么一开始要讲斐波那契数列,因为它非常适合模拟cpu密集的情况
    1.我这里实现了一个计算fib的函数时间复杂度是O(2^n)
    2.稍微解释下这个概念
    3.例如：计算1要1微秒，10就需要1毫秒，20需要1秒，30要1000秒，100要14671881947085988443天
    4.验证下这个概念
    1.ipython -i fib.py
    2.验证数字1 10 20 30 35 38
    6.看一下是不是要黑一下PHP
    （讲一个事情，真事，不是黑，不要因为一般学习各门语言编程书一般都会有个计算fib数的例子吧，c python go rust java，
     我有一天发了个计算各语言fib性能对比的博客给我朋友看，我朋友说fib是啥，我很诧异，我说你写代码，或者看代码书的
     时候都没有接触过吗？他说我们写PHP的不需要这个）
-->

<!--
开始对外提供服务的概念
    0.fib适合模拟cpu密集的情况
    1.现在我还需要模拟一个i/o密集的情况用作对照
    3.i/o包括读写磁盘，网络传输
    4.我这里用网络传输来模拟io
    5.所以 我现在准备对外提供这个计算fib的微服务
-->
  
#### 单线程
<!--```python
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
-->
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

现象，只能对一个客户端服务
<!--
为什么只能服务一个客户端
    0.讲讲单线程
-->

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
listen -> recv -> compute -> 

单线程是一个有原则的人，他同一个时间只为一个人服务,有原则并不代表专一

原则:

1.谁先来为谁服务

2.上一个走了才能为下一个人服务
<!--
我们如何让它服务多个客户端，任何服务都是需要服务多客户端的
    1.类比生活中的例子
    0.所以我们需要多线程
    2.开始一顿操作
    3.先使用nc 让大家看到可以两个同时连接上去
    4.多线程
    5.开始性能测试
    6.第二个客户端链接上之前提问大家，性能会有什么变化
    6.对比I/O密集 CPU密集情况下处理第二个客户端的性能变化
    7.引出GIL
-->

#### 多线程

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

<!--```python
# thread_server.py
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
-->
我们这个服务不可能只对一个用户提供，所以需要多线程，每个线程依旧遵循上面的原则

#### GIL
![Python多线程](/images/Python多线程.gif "Python多线程")
为什么会有GIL,因为Python的内存管理不是线程安全的
啥是线程安全，这个后面讲，在引出Python的内存管理之后
python多线程是鸡肋，由于GIL的存在只能利用一个CPU? 
实际上GIL是Cpython的



#### 内存管理
一个场景，学校有一些办公场所用于租给各个部门协会，
办公场所是有限的，每个协会/部门及任何人都可以租用场地，
允许共用一块场地，
当一个场地没有任何人使用时需要进行回收，然后等待其他部门申请用于其他的用途
你会如何管理这些场地的分配和回收？
0.直接申请，不要的时候再告诉学校，如果你忘记了，这块空间就一直处于不可以用的情况
1.定时询问，比如每周五询问一次有没有人使用，全部统计结束前的时候不允许分配场地，避免出现刚才统计结果不一致
这种方法需要停止所有场地的分配，还要询问等待所有人回复 go
2.引用计数，竞争，因为分配和增加引用时很频繁的，频繁的锁解锁十分的影响性能，所以有了GIL cpython
3.拥有权，部门协会申请后在某个区间范围内可以使用这片区域，例如有个活动开始申请，活动结束立马就回收 rust


#### 多进程
```
+---------------------+       +----------------------------------------+
    Process Pool      |       | Process                                |
                      |       |                                        |
      +-----------+   |       |                            thread1     |
      |Process1   |   |       |                          +----------+  |
      |   +-----+ |   |       |                          |   recv   |  |
      |   | GIL | |   |       |                          |    +     |  |
      |   +-----+ |   |  <--------------------------------+ submit  |  |
      +-----------+   |       |                          |    +     |  |
                      |  +--------------------------------> result  |  |
      +-----------+   |       |                          |    +     |  |
      |Process2   |   |       |                          |   send   |  |
      |   +-----+ |   |       |                          +----------+  |
      |   | GIL | |   |       |                                        |
      |   +-----+ |   |       |                            thread2     |
      +-----------+   |       |                          +----------+  |
                      |       |                          |   recv   |  |
      +-----------+   |       |                          |    +     |  |
      |Process3   |   |  <--------------------------------+ submit  |  |
      |   +-----+ |   |       |                          |    +     |  |
      |   | GIL | |   |  +--------------------------------> result  |  |
      |   +-----+ |   |       |                          |    +     |  |
      +-----------+   |       |                          |   send   |  |
                      |       |   +-------+              +----------+  |
            X         |       |   |       |                            |
                      |       |   |  GIL  |     其 余 部 分 同多 线 程 版 本     |
            X         |       |   |       |                            |
                      |       |   +-------+                            |
            X         |       |                                        |
 +--------------------+       +----------------------------------------+


```
<!--```python
# multiprocess_server.py
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
-->

多进程fork的方式 实际上非常的慢,消耗很多资源



#### 协程
```python
   +
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
<!--```python
# async_server.py

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
        future = pool.submit(fib, n)
        yield 'future', future
        result = future.result()    #  Blocks
        # result = fib(n)
        resp = str(result).encode('ascii') + b'\n'
        yield from client.send(resp)  # blocking
    print("Closed")


tasks.append(fib_server(('', 25000)))
run()
-->
一个人只能为一个客户服务，这样太浪费了，为什么不能做个渣男，同时和多个人聊天？


#### 未来绕过GIL的方案
<!--```python
# server.py
# Fib microservice
# Use Python 3

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

-->


#### 讲都讲了，分析一下应用场景

I/O 密集情况下:

代码    | 1个客户端    | 2个客户端
:---- | :---- | :----
one_server | 12 000 reqs/sec | 无法对外提供服务
thread_server |  12 000 reqs/sec  |  16 000 reqs/sec
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



#### python vs golang
<!--```go
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
-->
<!--```python
# many_server.py
# Use Python 3

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

port = sys.argv[1]
fib_server(('', int(port)))

-->

国内很多大厂迁移到go或者重度使用go,性能，不能利用多核，太废内存
为此google甚至启动了一个疯狂的项目


11.Python vs Other

#### 扩展阅读:
CPU绑定和IO绑定
https://stackoverflow.com/questions/868568/what-do-the-terms-cpu-bound-and-i-o-bound-mean

原味视频 https://www.youtube.com/watch?v=MCs5OvhV9S4

GIL已死https://medium.com/hackernoon/has-the-python-gil-been-slain-9440d28fa93d

啥是GILhttp://cenalulu.github.io/python/gil-in-python/

在线编程https://github.com/sloria/doitlive

为什么要GIL https://juejin.im/post/5d174d1af265da1b6a34aa05

CPYTHON 源码安装 https://realpython.com/cpython-source-code-guide/

源码https://github.com/tonybaloney/cpython/tree/subinterpreters/Lib
google疯狂的项目
https://github.com/google/grumpy
InfoQ 稍微讲下 grumpy
https://www.infoq.cn/article/2017/01/Grumpy-Google-Go-Python
Python写时复制 (引用计数导致多进程程无法利用写时复制)
译文
https://learnku.com/python/t/22973/instagram-actual-combat-exploring-write-time-replication-friendly-python-garbage-collection-mechanism
原文
https://instagram-engineering.com/dismissing-python-garbage-collection-at-instagram-4dca40b29172