---
title: "使用Horizon构建自定义的Dashboard"
date: 2019-09-22T15:55:49+08:00
draft: true
---


本章主要讲解如何使用Horizon创建一个你自己的Dashboard
<!--more-->

#### 快速构建

这里可以用官方提供的构建工具去快速创建好一个模板，如果本地没有下载和配置tox也没关系，直接按照本文章
后面贴出的代码及文件名对应文件树的位置进行创建。

```
$ mkdir openstack_dashboard/dashboards/mydashboard

$ tox -e manage -- startdash mydashboard \
  --target openstack_dashboard/dashboards/mydashboard

$ mkdir openstack_dashboard/dashboards/mydashboard/mypanel

$ tox -e manage -- startpanel mypanel \
  --dashboard=openstack_dashboard.dashboards.mydashboard \
  --target=openstack_dashboard/dashboards/mydashboard/mypanel
```

#### 构建完成文件树结构

```
mydashboard
├── dashboard.py
├── __init__.py
├── mypanel
│   ├── __init__.py
│   ├── panel.py
│   ├── templates
│   │   └── mypanel
│   │       └── index.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static
│   └── mydashboard
│       ├── css
│       │   └── mydashboard.css
│       └── js
│           └── mydashboard.js
└── templates
    └── mydashboard
        └── base.html
```

#### 创建Dashboard

打开或者创建一个包含以下内容的dashboard.py文件
```python
from django.utils.translation import ugettext_lazy as _

import horizon


class Mydashboard(horizon.Dashboard):
    name = _("Mydashboard")
    slug = "mydashboard"
    panels = ()           # Add your panels here.
    default_panel = ''    # Specify the slug of the dashboard's default panel.


horizon.register(Mydashboard)
```

该文件中name声明了Dashboard的名称，内部组件互相引用使用的是slug的名称,你可以
在这里添加panels，和设置默认的panel。

注： 新版本中Panel和PanelGroup统一通过plugin的方式进行注册，相关配置文件在openstack_dashboard/enabled下，
Dashboard仅专注与panel相关功能的实现.

#### 创建Panel

mypanel的文件树
```
mypanel
 ├── __init__.py
 ├── models.py
 ├── panel.py
 ├── templates
 │   └── mypanel
 │     └── index.html
 ├── tests.py
 ├── urls.py
 └── views.py
```

打开或者创建一个包含以下内容的panel.py文件
```python
from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.mydashboard import dashboard


class Mypanel(horizon.Panel):
    name = _("Mypanel")
    slug = "mypanel"


dashboard.Mydashboard.register(Mypanel)
```

打开dashboard.py把下面代码插入到Mydashboard class的上方
```python
class Mygroup(horizon.PanelGroup):
    slug = "mygroup"
    name = _("My Group")
    panels = ('mypanel',)
```

修改Mydashboard类去包含我们添加的Mygroup
```python
class Mydashboard(horizon.Dashboard):
   name = _("My Dashboard")
   slug = "mydashboard"
   panels = (Mygroup,)  # Add your panels here.
   default_panel = 'mypanel'  # Specify the slug of the default panel.
```

修改完成后的dashboard.py 如下所示
```python
from django.utils.translation import ugettext_lazy as _

import horizon


class Mygroup(horizon.PanelGroup):
    slug = "mygroup"
    name = _("My Group")
    panels = ('mypanel',)


class Mydashboard(horizon.Dashboard):
    name = _("My Dashboard")
    slug = "mydashboard"
    panels = (Mygroup,)  # Add your panels here.
    default_panel = 'mypanel'  # Specify the slug of the default panel.


horizon.register(Mydashboard)
```

#### 表、选项卡、构建视图

Horizon提供DataTable类用于处理表相关功能的抽象类，
我们只需要填写几个属性就可以使用复用DataTable所提供的功能

创建一个tables.py在mypanel目录下并添加如下代码
```python
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class InstancesTable(tables.DataTable):
    name = tables.Column("name", verbose_name=_("Name"))
    status = tables.Column("status", verbose_name=_("Status"))
    zone = tables.Column('availability_zone',
                          verbose_name=_("Availability Zone"))
    image_name = tables.Column('image_name', verbose_name=_("Image Name"))

    class Meta(object):
        name = "instances"
        verbose_name = _("Instances")
```
我们创建了一个DataTable的字类，这里声明了几个属性
tables.Column的第一个参数用来访问实例对象，
verbose_name在展示的时候用到，你可以自行修改然后重启
horizon服务查看页面渲染的结果，Meta里面的instances对应数据
表的名称。

我们这里为table添加一个过滤的动作，首先我们需要声明一个动作
```python
class MyFilterAction(tables.FilterAction):
    name = "myfilter"
```
把MyFilterAction添加到InstancesTable中
```python
class InstancesTable:
    class Meta(object):
        table_actions = (MyFilterAction,)
```

完整的tables.py文件如下所示
```python
from django.utils.translation import ugettext_lazy as _

from horizon import tables


class MyFilterAction(tables.FilterAction):
    name = "myfilter"


class InstancesTable(tables.DataTable):
    name = tables.Column('name', \
                         verbose_name=_("Name"))
    status = tables.Column('status', \
                           verbose_name=_("Status"))
    zone = tables.Column('availability_zone', \
                         verbose_name=_("Availability Zone"))
    image_name = tables.Column('image_name', \
                               verbose_name=_("Image Name"))

    class Meta(object):
        name = "instances"
        verbose_name = _("Instances")
        table_actions = (MyFilterAction,)
```

#### 定义选项卡

创建tabs.py文件,完整代码如下
```python
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.mydashboard.mypanel import tables


class InstanceTab(tabs.TableTab):
    name = _("Instances Tab")
    slug = "instances_tab"
    table_classes = (tables.InstancesTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def has_more_data(self, table):
        return self._has_more

    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                        tables.InstancesTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []

class MypanelTabs(tabs.TabGroup):
    slug = "mypanel_tabs"
    tabs = (InstanceTab,)
    sticky = True
``` 
preload=False代表只有在点击的时候才会以AJAX方式加载数据，这种方式可以减少不必要的调用，
api.nova.server_list会调用novaclient发送http请求到nova，然后查询数据库，最后返回结果。

#### 创建视图函数
tabs.TabbedTableView类可以更好的配合table和tabs做页面渲染及展示，更多tabs.TabbedTableView相关的
可以在文末找到资料

```python
from horizon import tabs

from openstack_dashboard.dashboards.mydashboard.mypanel \
    import tabs as mydashboard_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    template_name = 'mydashboard/mypanel/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
```

### 其他文件

url.py
```python
from openstack_dashboard.dashboards.mydashboard.mypanel import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
```

index.html
```
{% extends 'base.html' %}
{% load i18n %}
{% block title %}{% trans "My Panel" %}{% endblock %}

{% block page_header %}
   {% include "horizon/common/_page_header.html" with title=_("My Panel") %}
{% endblock page_header %}

{% block main %}
<div class="row">
   <div class="col-sm-12">
   {{ tab_group.render }}
   </div>
</div>
{% endblock %}
```

TODO: 这里还有几个文件没有写进来


#### 使代码生效
为了使上面所添加的配置生效你需要在 openstack_dashboard/enabled创建一个_50_mydashboard.py文件
```python
# The name of the dashboard to be added to HORIZON['dashboards']. Required.
DASHBOARD = 'mydashboard'

# If set to True, this dashboard will not be added to the settings.
DISABLED = False

# A list of applications to be added to INSTALLED_APPS.
ADD_INSTALLED_APPS = [
    'openstack_dashboard.dashboards.mydashboard',
]
```

重启服务,然后用浏览器打开dashboard就看mydashboard了。

#### 参考文章及推荐阅读

* 本文章基于
[Building a Dashboard using Horizon](https://docs.openstack.org/horizon/rocky/contributor/tutorials/dashboard.html)，
如果想为table添加更加复杂的行为可以查看
[Adding a complex action to a table](https://docs.openstack.org/horizon/rocky/contributor/tutorials/table_actions.html)

* 《OpenStack设计与实现》第11章对Horizon进行了比较全面的讲解