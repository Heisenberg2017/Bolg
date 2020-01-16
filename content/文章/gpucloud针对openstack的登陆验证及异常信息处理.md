---
title: "gpucloud针对openstack的登陆验证及异常信息处理"
date: 2019-12-26T11:25:00+08:00
draft: true
---

gpucloud针对openstack的登陆验证及异常信息处理
<!--more-->

#### 一个常见的例子


这是一个销毁卷的接口,调用的流程是这样的:

 * 先进行keystone认证，根据传入的username验证，验证失败抛出异常
 * 验证通过调用删除接口，删除成功调用完成
 * 删除失败会打印异常信息，接口返回一些有助debug的信息
```python
    def destroy(self, request, pk=None):
        """
        删除卷
        ...
        """

        volume_id = pk
        username = request.data.get('username') if request.data.get('username') else "admin"
        request, os_username = openstack_user_auth.user_auth(request, username)
        if not request:
            return res.error_status(VolumeStatus.VOLUME_10600_AUTH_FAIL)
        
        try:
            api.cinder.volume_delete(request, volume_id)
        except Exception as e:
            LOG.error(e)
            return res.error_status(global_status.GC_1002_OPENSTACK_INTERNAL_ERROR)

        return res.success()
```

#### OpenStack内部调用失败如何处理

以下是删除失败的接口返回信息
```python
{
  "msg": "Openstack Internal error",
  "code": 1002,
  "data": null
}
```
删除失败信息说是openstack内部调用错误，然后就没有然后了。

这个时候开发人员从测试或者另一端开发人员那里收到这个失败信息，开始tail -f 或者
vi ...疯狂查找错误可能发生的位置,这个debug可能会从apache2/horizon.log -> apache2/gpucloud.log -> gpucloud.log -> xxx.log ...

如果有幸在进入openstack内部组件的xxx.log前就确定了request_id（OpenStack的全局唯一ID）

那就可以grep -r req_id-xxxxxxxx /var/log 查看到对应的日志信息,如果幸运的话找出BUG解决问题

#### 这个流程有没有问题?

从开发到debug这个流程都是正确的，但是接口太多代码是冗余的，每个接口都有太多和业务逻辑无关的信息，
用户验证，异常处理，即使写了异常处理，debug也非常的不便。

#### 期望

1.我不希望每个接口都需要添加和业务无关的keystone认证，

2.我也不希望每个接口都要捕获openstack的异常，太多相同的代码要写了，但是不捕获又会报500，

3.捕获异常后返回的调用信息其实对DEBUG帮助并不大

#### 如何改进

针对问题1OpenStack登陆验证的部分 目前我使用装饰器实现了两种登陆方式

1.需要用户名的验证方式,这个时候默认使用request.data['username']对应用户进行登陆
验证
```python
@openstack_user_auth.keystone_auth()
def foo(self, request, pk=None):
    # 这个时候request请求中已经有token了，可以直接访问OpenStack
    pass
```

2.admin用户，例如做一些删除操作
验证
```python
@openstack_user_auth.keystone_auth(admin=True)
def foo(self, request, pk=None):
    # 这个时候request请求中已经有token了，可以直接访问OpenStack
    pass
```

如果你需要从OpenStack验证中带出一些信息到接口中,可以在装饰器实现里添加任意信息到keystone_auth里面
例如: request.keystone_auth['foo'] = foo 这样接口就可以通过request直接访问你保存的值了

针对问题2 OpenStack内部异常处理，这里有两个问题，一是我不想每个接口都去捕获异常，二是异常信息太少，不方便debug

我统一使用中间件处理这个问题，view中抛出的异常，如果是OpenStack的，进行处理，并返回完整的异常信息,不是则继续向上抛出，
如果需要细分OpenStack抛出的异常可以在代码注释处仿照处理

```python
class OpenStackExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        LOG.info('OpenStack Exception:%s', exception)

        # 非OpenStack异常不处理
        if not getattr(exception, 'request_id'):
            raise exception

        # exception_class = exception.__class__
        # if exception_class == FooException:
        #     do something

        traceback_exc = traceback.format_exc() if settings.DEBUG else None

        return res.error_status(
            error_status=GC_1002_OPENSTACK_INTERNAL_ERROR,
            exception={
                "name": repr(exception),
                "code": exception.code,
                "details": exception.details,
                "message": exception.message,
                "request_id": exception.request_id,
                "traceback_exc": traceback_exc
            },
        )

```
当DEBUG=True时，会返回完整的调用栈信息，这个时候你需要把traceback_exc对应的值复制到命令行使用print(traceback_exc)才能看到换行的异常栈信息


#### 改进之后

改进后的接口代码, 从原先的11行到2行，看起来很清晰，可读性++，成功直接返回删除成功

```python
    @openstack_user_auth.keystone_auth(admin=True)
    def destroy(self, request, pk=None):
        """
        删除卷
        ...
        """

        api.cinder.volume_delete(request, pk)

        return res.success()
```

再看看接口调用异常的返回值
```python
{
  "msg": "Openstack Internal error",
  "exception": {
    "code": 404,
    "name": "NotFound()",
    "details": "n/a",
    "request_id": "req-53e90992-ad28-45e7-adc6-05b7323cac1c",
    "traceback_exc": null,
    "message": "Volume asdada could not be found."
  },
  "code": 1002,
  "data": null
}
```
除了内部调用失败外还多了openstack内部调用的详细异常信息,直接看异常信息就可以看出asdada的卷是不存在的，
你不能删除一个不存在的卷

还有更多信息例如request_id, 有了它就可以找到内部调用的日志信息了

内部调用有太多异常可能发生，你只需要处理你想处理的异常，其他就直接交给中间件，抛出去就完事了


#### 你可能要知道的事情

如果你是开发人员，可以尝试DEBUG=True，看看完整的异常信息，这样开发或许更快

如果你是测试人员，如果看了异常信息还不明白，复制给开发，开发会通过request_id或者exception中的其他信息去解决这个bug

如果你需要调用gpucloud的接口，你应该要知道我们新增了exception字段，如果要配合后期的bug追踪，你们可以保存请求对应的request_id这个对后期异常处理有很大帮助

如果对Python感兴趣，看看装饰器和Django中间件，这个文档就是使用这两个解决代码冗余