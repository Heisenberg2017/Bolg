---
title: "WATCHPIG效率工具"
date: 2020-01-16T11:13:52+08:00
draft: false
---

针对远程开发及修改代码需要执行对应命令的场景
<!--more-->

#### 我的开发场景

1.在一个需求开发中需要修改的组件很多，修改完需要重启各个组件代码才会生效

2.我可能需要频繁修改代码，频繁重启组件才能完成一次开发任务

3.我在Win10上开发，代码会同步到远程的开发服务器上

#### 痛点

1.每次变更代码后需要重启才能生效，偶尔会出现忘记重启

2.修改涉及多个组件，每个组件需要执行的命令不同

3.我要记住修改的文件位置对应需要执行的命令，一个地方未执行就可能导致服务报错，这个时候我需要花时间DEBUG,可能十几分钟后才发现是忘记执行重启命令导致的

4.没有一个清晰的反馈，更新了哪些文件，执行成功或者失败，执行时间


#### 为什么自己写

Django有autoreload模块，文件监控做的比较好的有watchdog，开箱即用不好吗？

1.不希望引入第三方依赖

2.本身功能简单，需要花费时间较少

2.我需要做一些定制，例如输出emoji，字体渲染之类

#### 使用WATCHPIG

1.下载源码
```shell script
git clone https://github.com/Heisenberg2017/watchpig.git
```

2.查看配置文件
```shell script
vi vi watchpig/monitor.conf
```

单个监控单元配置如下
```shell script
[::EMOJI::nova|| nova]
path = /usr/lib/python2.7/dist-packages/nova
action = service nova-api restart
excludes = .*\.mo
```
path为监控的目录，当监控目录有文件变化时，会执行对应的action
excludes用来排除你不需要监控的文件后缀，这个例子中.mo后缀的文件即使发生变化也不会执行对应action

[]中的为项目描述，这些奇怪字符作用会在后面说明

3.配置环境变量
你可以临时配置或者写在.bashrc中
下面是临时配置:
```shell script
export WATCHPIG=/root/watchpig/monitor.conf
```

4.运行

```shell script
root@osd6:~# python watchpig/src/watchpig/main.py monitor
```

5.操作并查看输出

![WATCHDOG运行示例](/images/WATCHDOG运行示例.png "WATCHDOG运行示例")

第一部分为启动的信息，输出中包含代表项目图标的emoji,项目名称

第二部分包含文件变更信息，及命令执行情况，这里执行失败，所以是愤怒的emoji

第三部分为命令执行成功后的情况

这个应用基本满足我的要求,让我不需要关心服务是否重启，思考更新了哪些文件，什么时候执行的，

简单且带高亮带emoji的输出让我可以更快的获得信息，而不是在一堆无重点且难以辨认的日志信息查找我要的信息

例如下面的变更信息,我真的不关心是10kbit/s还是20kbit/s
```shell script
[2020/1/16 16:02] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\common\rabbitmq_client.py' to '/tmp/pycharm_project_650/gpucloud/common/rabbitmq_client.py'
[2020/1/16 16:02] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\common\subject.py' to '/tmp/pycharm_project_650/gpucloud/common/subject.py'
[2020/1/16 16:02] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\common\management\commands\resource_report.py' to '/tmp/pycharm_project_650/gpucloud/common/management/commands/resource_report.py'
[2020/1/16 16:02] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\gpucloud\settings.py' to '/tmp/pycharm_project_650/gpucloud/gpucloud/settings.py'
[2020/1/16 16:02] Automatic upload completed in 35 ms: 4 files transferred (542.8 kbit/s)
[2020/1/16 16:17] Automatic upload
[2020/1/16 16:17] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\common\rabbitmq_client.py' to '/tmp/pycharm_project_650/gpucloud/common/rabbitmq_client.py'
[2020/1/16 16:17] Automatic upload completed in 30 ms: 1 file transferred (74.1 kbit/s)
[2020/1/16 16:19] Automatic upload
[2020/1/16 16:19] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\common\rabbitmq_client.py' to '/tmp/pycharm_project_650/gpucloud/common/rabbitmq_client.py'
[2020/1/16 16:19] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\common\subject.py' to '/tmp/pycharm_project_650/gpucloud/common/subject.py'
[2020/1/16 16:19] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\common\management\commands\resource_report.py' to '/tmp/pycharm_project_650/gpucloud/common/management/commands/resource_report.py'
[2020/1/16 16:19] Upload file 'D:\Users\thinkpad\OpenStackCode\openstack-gpucloud\gpucloud\gpucloud\settings.py' to '/tmp/pycharm_project_650/gpucloud/gpucloud/settings.py'
[2020/1/16 16:19] Automatic upload completed in 60 ms: 4 files transferred (316.6 kbit/s)
```

#### 自定义输出

如果需要添加/修改/删除emoji怎么做？在你的命令行中不兼容emoji输出乱码很烦人如何解决？

这里我们需要先了解paint，这是我们为文字变更颜色及添加emoji的关键
到watchpig所在的目录下面执行命令
```shell script
ipython -i watchpig/src/watchpig/painter.py
```

![WATCHDOG上色](/images/WATCHDOG上色.png "WATCHDOG上色")

paint基本用法就在这里

格式为{字符}::{变量名}::{变量字典对应的key}

第一个::前面为需要处理的字符，允许重复上色，emoji表情的::前面不允许有任何字符，需要分段处理用||隔开

下面为watchpig/src/watchpig/painter.py中的EMOJI变量，
如果你修改对应的表情，脚本输出也会对应修改，
你还可以添加自己的表情，增加对应的key即可，
如果其中一个EMOJI是乱码直接替换或者用u' '代替例如下面的foo

```shell script

EMOJI = {
    "pig": u'🐷',
    "time": u'🕒',
    "separator": u'➖',
    'succeed': u'😃',
    'failed': u'😡',
    "run": u'🚀',
    "change": u'📝',

    "translate": u'💬',
    "dashboard": u'🌏',
    "horizon": u'🌏',
    "novaclient": u'🌟',
    "nova": u'🌟',
    "glance": u'💿',
    "cinder": u'💾',
    "gpucloud": u'🌈',
    "foo": u' ',
}
```

#### 如何查找自己的EMOJI

如果你不知道如何查找自己喜欢的可以使用自带的
我们用这个命令查一下名称中带face的emoji，最好在你运行监控脚本的窗口中执行，这样也可以知道你的终端是否支持这个表情的展示
```shell script
python watchpig/src/watchpig/main.py emoji --search face
```

![查找emoji](/images/查找emoji.png "查找emoji")

找到表情后直接复制到
watchpig/src/watchpig/painter.py->EMOJI->然后添加一个key和emoji，你也可以替换你不要的emoji


#### 环境

1.Win10+、CentOS6+、Ubuntu18.04都自带了EMOJI的支持

2.Python2.7 不支持Python3, 因为我目前的开发环境都是python2.7

3.可以运行在CentOS6+、Ubuntu18.04理论上linux都可以，不支持Win10