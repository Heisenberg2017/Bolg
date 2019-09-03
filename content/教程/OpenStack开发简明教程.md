---
title: "OpenStack开发简明教程"
date: 2019-08-31T18:19:42+08:00
draft: false
---

这一系列是面向OpenStack二次开发的新手教程，目前是让看完教程并实践的同学对OpenStack开发有初步的认识，再稍加练习可以投入企业的云计算项目开发中去。
<!--more-->

#### 教程目的

让学员可以更快的参与到项目开发中去，会适当提到OpenStack的设计及实现相关知识，但OpenStack设计与实现已经超出此系列教程的范围，所以这部分
不会深入讲解，仅会在段落或者文章末尾贴出链接让大家自行学习。

#### 学习本教程需要
* Python基础
* linux基础
* 善用搜索引擎
* 持之以恒



#### 如果没有特殊说明本系列教程所有代码都运行在以下环境
* OpenStack Version: Rocky
* VMware 14
* 操作系统: CentOS 7
* IDE： Pycharm 2019.9.2

#### 系统(虚拟机)配置推荐

* 内存 8~16G
* 硬盘 20~40G
* CPU 1个以上

#### 一些配置经验
部署OpenStack(all in one)本地测试环境时需要较大的内存，如果是在虚拟机内部署
OpenStack至少的需要8G以上的内存及单核心单线程，如果OpenStack和IDE在同一环境，建议内存在16G以上，
**虚拟机的内存和核心数（尤其是内存）会极大影响安装及部署的效率**，我目前虚拟机配置的内存是16G，双核四线程，40G硬盘容量，
使用中内存占用率一般在6G-10G之间，如果内存不足会发生swap进而极大的影响开发效率。

#### 注意点

一些环境的安装例如VMware、Pycharm之类或者其他已经有很多安装教程的软件会直接贴出安装教程的链接，并提示一些要注意的地方。


#### 本教程遵循下面的原则
> Talk is cheap. Show me the code.

#### 教程目录

[开发环境搭建](https://heisenberg2017.github.io/%E6%96%87%E7%AB%A0/openstack%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA/).

[控制面板之Horizon](https://duckduckgo.com).

[计算之Nova](https://duckduckgo.com).

[Openstack Rsst](https://duckduckgo.com).