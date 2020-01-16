---
title: "OpenStack代码修改规范 公司内部"
date: 2019-10-12T11:25:45+08:00
draft: true
---

公司内部项目OpenStack代码修改规范
<!--more-->
#### 功能的新增和修改
例子如下

这是OpenStack的源代码,实例详情页有四个tab
```python
class InstanceDetailTabs(tabs.DetailTabsGroup):
    slug = "instance_details"
    tabs = (OverviewTab, InterfacesTab, LogTab, ConsoleTab, AuditTab)
    sticky = True
```
horizon视图如下
![开发前实例页](/images/开发前实例页.png "开发前实例页")

目前产品有一个需求，需要对这个详情页进行修改，他要求掉当前页面，然后这个页面需要改成显卡详情页，
如果你完全按照产品需求实现修改代码如下
```python
class InstanceDetailTabs(tabs.DetailTabsGroup):
    slug = "instance_details"
    tabs = (VideoInfoTab, )
    sticky = True
```
这个时候页面展示是符合产品要求的，但是在开发人员的视角里面，很多功能缺失了(概况，接口，日志)，之后的版本这些功能都缺失了，
在版本迭代后，功能就永久缺失了，而且删除了源码，出现异常很难定位，难以回退。

为了更好的开发和符合产品要求，我们在配置文件添加USER_VIEW变量，通过USER_VIEW=True来开启用户视图，也就是产品经理要求
的视图

正确代码如下
```python
class InstanceDetailTabs(tabs.DetailTabsGroup):
    slug = "instance_details"
    if getattr(settings, 'USER_VIEW', False):
        tabs = (VideoInfoTab, )
    else:
        tabs = (OverviewTab, InterfacesTab, LogTab, ConsoleTab, AuditTab, VideoInfoTab)
    sticky = True
```
当前开发视图(没有USER_VIEW参数或者USER_VIEW=False的页面)
![开发后非用户视图实例页](/images/开发后非用户视图实例页.png "开发后非用户视图实例页")
开发视图功能都在，且新增的tab也能看到,供开发调试

当前用户视图(USER_VIEW=True的页面)
![开发后用户视图实例页](/images/开发后用户视图实例页.png "开发后用户视图实例页")
用户视图展示的是产品需要的视图,可提供测试使用

我们使用getattr(settings, 'USER_VIEW', False)来获取参数
settings是由以下代码导入的from django.conf import settings,
OpenStack配置也是这么引入的，统一使用getattr(settings, 'USER_VIEW', False)更重要的
地方是，即使没有这个参数也不会报错，并且切换用户的开发视图这个过程后来可能集成在horizon的界面
的设置里面，便于之后的批量修改.