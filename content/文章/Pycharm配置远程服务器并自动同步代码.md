---
title: "Pycharm配置远程服务器并自动同步代码"
date: 2019-09-20T14:59:23+08:00
draft: false
---
本章主要讲解如何使用Pycharm配置远程服务器并自动同步代码.
<!--more-->

#### 注意事项

* Pycharm的Deployment目前只有专业版才支持这个功能
* 使用Deployment请确保远程服务器打开了stfp

#### 应用场景
这里就说一下自己的例子，目前虚拟内搭建了一个OpenStack的All-in-One环境，
宿主机是Win10,由于可能会在不同的虚拟机内进行开发，所以一般不在虚拟机安装IDE进行本地开发，
这个时候我们就要在宿主机进行开发。

#### 准备工作

1.首先在你的本地环境新建一个文件用于存放项目代码,我这里命名为OpenStackCode

2.把项目代码拉到本地这个OpenStackCode目录里面,项目结构如下
thinkpad目录下的OpenStackCode就是我们步骤1创建的目录，
(目前我操作的还是本地文件，可以使用tree等命令是因为我是在WSL系统内切换到Win10的目录下，也就是/mnt，
你可以直接在win10下新建目录和使用git clone操作的结果是一样的）

![项目代码结构](/images/项目代码结构.png "项目代码结构")

目前我在本地需要修改的项目源码是openstack_dashboard这个目录
```shell script
OpenStackCode/openstack-horizon/python-django-horizon/usr/lib/python2.7/dist-packages/openstack_dashboard
```
对应的远程的代码路径是
```shell script
/usr/share/openstack-dashboard/openstack_dashboard
```

#### 同步配置



1.创建新的Pycharm项目
![创建新项目](/images/创建新项目.png "创建新项目")
本地目录就是我们要在本地修改的项目目录，也就是你git clone下来的那个目录,
其他设置选择默认的就行，Python的环境我们会在后面设置成远程的开发环境。

由于我们是创建一个非空的项目，所以这我们选择No不替换源文件
![是否替换源文件](/images/是否替换源文件.png "是否替换源文件")

2.配置远程服务器Deployment

tools->Deployment->configuration

点右上角的“+”添加服务器信息，服务器类型选择SFTP，输入项目名

![连接设置](/images/连接设置.png "连接设置")

这里填上对应的远程服务器ip，用户名，密码，Root Path这里我们选择默认的，
后续做文件映射时候就是以这个目录作为远程文件的根目录来做映射。

3.选择Mappings

这个步骤是比较重要的一块，在这里设置文件目录映射之后就可以在本地和服务器
上进行文件同步了

![文件映射](/images/文件映射.png "文件映射")

这里我是把本地目录

OpenStackCode/openstack-horizon/python-django-horizon/usr/lib/python2.7/dist-packages/openstack_dashboard

映射到远程服务器的

OpenStackCode/openstack-horizon/python-django-horizon/usr/lib/python2.7/dist-packages/openstack_dashboard
目录

配置完成后你在本地目录所作的修改就可以通过Deployment来进行同步,
你可以自行设置自动同步或者仅同步部分文件，也可以添加新的映射。

![同步设置](/images/同步设置.png "同步设置")

#### 配置Python解释器

点击Pycharm->Settings->Project->Python Interpreter点击齿轮图标

![设置远程Python环境](/images/设置远程Python环境.jpg "设置远程Python环境")

这里选择SSH Interpreter 填上对应的远程主机信息 然后点击Next
![设置Python路径](/images/设置Python路径.png "设置Python路径")

这里选择你的python解释器所在的位置，点击Finish，至此配置远程服务器启动并同步代码就完成了。

#### 参考资料
* [Pycharm远程部署及调试](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html)
Pycharm官方文档，这里用一个小例子来介绍如何使用Pycharm进行远程部署及调试
* [Pycharm专业版配置远程服务器并自动同步代码](https://blog.csdn.net/wz22881916/article/details/82670969)
CSDN上的一个有关远程代码同步的文章
