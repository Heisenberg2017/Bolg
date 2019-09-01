---
title: "OpenStack开发环境搭建"
date: 2019-08-31T19:32:42+08:00
draft: true
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

CentOS 7国内环境官方下载比较慢，这里可以选择镜像
[CentOS 7国内镜像](https://duckduckgo.com).


#### 部署All-in-One

在开始部署前你需要完整看完[rdo OpenStack All-in-One 环境部署](https://www.rdoproject.org/install/packstack/)，
注意我们安装的是Rocky版本，
需使用openstack-rocky替换教程中的openstack-stein，
[OpenStack相关版本](https://releases.openstack.org/)，国内用户安装可以替换yum源以提高下载速度
[使用阿里的yum镜像](https://duckduckgo.com).。


本地部署完成后你应该可以打开(dashboard网址)，这里还需要添加一个 --enable-....txt的事情

#### 工作环境

IDE的话我们选择Pycharm，由于日常工作中可能会经常使用不同的虚拟机来部署不同的组件，
所以我会把IDE安装在Win10上，然后使用Pycharm自带的文件同步服务(基于fstp)和远程Debug服务(基于pydev)
进行开发与调试,具体参考[Pycharm的remote部署及调试](https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html).

#### 其他资料:

[OpenStack调查报告](https://www.openstack.org/analytics):
从中你可以看到OpenStack各个组件的发展趋势，用户的部署方式等等，让你对OpenStack当前的发展有一个比较清晰的认识。

[深入理解OpenStack自动化部署](https://pom.nops.cloud/Introduction/Intro.html):
这本书主要讲puppet,现在Ansible已经占OpenStack自动化部署的半壁江山，或许你应该学习Ansible。

Ansible相关:
[Ansible中文权威指南](https://ansible-tran.readthedocs.io/en/latest/docs/intro.html)、
[使用Ansible部署OpenStack](https://docs.openstack.org/project-deploy-guide/openstack-ansible/rocky/index.html)


