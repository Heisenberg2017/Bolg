---
title: "自己动手写Web框架"
date: 2019-08-27T21:42:32+08:00
draft: true
---
#### 什么是WSGI？
WSGI是应用程序和服务器的接口，更高级点的说法，WSGI让代码以更正式的方式传递Web请求。


下面是最简单的WSGI应用程序
```python
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['Hello World!']
```
environ类似CGI请求的环境
