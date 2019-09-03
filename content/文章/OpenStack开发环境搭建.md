---
title: "OpenStack开发环境搭建"
date: 2019-08-31T19:32:42+08:00
draft: false
---
OpenStack是一个复杂的技术栈组合，这一章节我们将使用PackStack
快速部署一个本地的All-in-One环境。
<!--more-->

#### 基本概念
All-in-One: 所有的服务部署到一台服务器上

Multi-Node: 控制节点和计算机分离

Puppet: Puppet公司开发的系统管理框架和工具集，
被用于IT服务的自动化管理。

PackStack: Redhat推出的用于概念验证（PoC）环境快速部署的工具。
他是一个命令行工具，它使用Python封装了Puppet模块，通过SSH在服务器上部署OpenStack。

#### 部署工具

PackStack和Puppet在16年的调查中市场占有率超过50%，不过后面Ansible风头更盛，这个章节并不打算对部署工具进行比较，
我们只是搭建一个本地的All-in-One节点，如果你对其他部署工具感兴趣可以参考2018年OpenStack集群部署工具问卷:

![2018年OpenStack集群部署工具问卷](/images/OpenStack部署工具调查.png "2018年OpenStack集群部署工具问卷")

#### 操作系统的安装

无论是官方或者其他部署工具都会告诉你尽量使用纯净的系统进行All-in-One部署，
我觉得你应该也不想花大量时间来解决系统的依赖问题，所以我们从操作系统安装开始

VMware14和CentOS 7的安装可以参考一下这篇博客[VMware14安装CentOS 7](https://duckduckgo.com).

CentOS 7国内环境官方下载比较慢，这里可以选择阿里的镜像
[CentOS 7国内镜像](http://mirrors.aliyun.com/centos/7.6.1810/).


#### 部署All-in-One

部署过程参考[rdo OpenStack All-in-One 环境部署](https://www.rdoproject.org/install/packstack/)，
注意我们安装的是Rocky版本，
需使用openstack-rocky替换教程中的openstack-stein，Openstack历史版本可以查看
[OpenStack相关版本](https://releases.openstack.org/)，国内用户安装可以替换yum源以提高下载速度
[使用阿里的yum镜像](https://www.jianshu.com/p/4aa7b63f9026)。

注意点：

1.安装一直卡在
```
openstack Testing if puppet apply is finished...
```
首先你应该要先检查yum是否使用了镜像，如果确认使用了镜像且网络没有问题的话，可以直接ctrl+c退出，重启电脑然后重新执行
```
sudo packstack --allinone
```
如果是在虚拟机内部署的All-in-One环境
可以分配更多的内存和CPU这样下载和启动速度都会快一点.

2.安装失败且已经生成answerfile 
如果安装失败但是在命令行中看到如下信息

```
* A new answerfile was created in: /root/packstack-answers-20190817-203646.txt
```

那么你下次安装的时候记得直接执行
 ```packstack --answer-file packstack-answers-20190817-203646.txt```
 这个时候packstack会根据已经生成的配置文件进行部署

安装完成后你可以看到如下输出
```
 Time synchronization installation was skipped. Please note that unsynchronized time on server instances might be problem for some OpenStack components.
* File /root/keystonerc_admin has been created on OpenStack client host 192.168.12.128. To use the command line tools you need to source the file.
* To access the OpenStack Dashboard browse to http://192.168.12.128/dashboard .
Please, find your login credentials stored in the keystonerc_admin in your home directory.
* The installation log file is available at: /var/tmp/packstack/20190818-091906-r_BX4u/openstack-setup.log
* The generated manifests are available at: /var/tmp/packstack/20190818-091906-r_BX4u/manifests
```
 
打开http://192.168.12.128/dashboard （具体IP查看部署命令输出）,你会看到如下界面
![Horizon登陆页](/images/Openstack登陆页面.png "Horizon登陆页")
你的页面颜色可能和我不一样，我这里使用了chrome的插件,用户名和密码在packstack-answers-20190817-203646.txt
的这个文件里面，你可以使用sudo find / -name "packstack-answers-*"查看这个配置文件的位置，打开这个文件找到下面的两行
```
# Password to use for the Identity service 'admin' user.
CONFIG_KEYSTONE_ADMIN_PW=97a7dd26984940ff

# Password to use for the Identity service 'demo' user.
CONFIG_KEYSTONE_DEMO_PW=63c2dd13d9154ab6
```
admin用户对应密码CONFIG_KEYSTONE_ADMIN_PW,

demo用户对应密码CONFIG_KEYSTONE_DEMO_PW

我们使用demo用户登陆,登陆成功后看到
![Horizon主页](/images/Horizon主页.png "Horizon主页")
这个时候All-in-One的环境就部署完成了，这里如果浏览器显示的是中文的话建议到浏览器的设置里面进行修改，
因为这里的命名和里面模块名有关，英文名称对你后面学习Horizon的开发会有帮助

#### 工作环境

如果只是打算在本地开发的话可以跳过这一个步骤,IDE的话我们选择Pycharm，由于日常工作中可能会经常使用不同的虚拟机来部署不同的组件，
所以我会把IDE安装在Win10上，然后使用Pycharm自带的文件同步服务(基于fstp)和远程Debug服务(基于pydev)
进行开发与调试,具体参考[Pycharm的远程部署及调试](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html).

#### 其他资料:

[OpenStack调查报告](https://www.openstack.org/analytics):
从中你可以看到OpenStack各个组件的发展趋势，用户的部署方式等等，让你对OpenStack当前的发展有一个比较清晰的认识。

[深入理解OpenStack自动化部署](https://pom.nops.cloud/Introduction/Intro.html):
这本书主要讲puppet,现在Ansible已经占OpenStack自动化部署的半壁江山，或许你应该学习Ansible。

Ansible相关:
[Ansible中文权威指南](https://ansible-tran.readthedocs.io/en/latest/docs/intro.html)、
[使用Ansible部署OpenStack All-in-One](https://docs.openstack.org/openstack-ansible/rocky/user/aio/quickstart.html)


