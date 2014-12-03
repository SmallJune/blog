#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *

urlpatterns = patterns('blog.sblog.views',
    (r'^bloglist/$', 'blog_list'),
    # name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url bloglist %}
    (r'/(?P<id>\d+)/$', 'blog_show'),
    (r'^/tag/(?P<id>\d+)/$', 'blog_filter'),
    (r'^/add/$', 'blog_add'),
    (r'^/(?P<id>\w+)/update/$', 'blog_update'),
    (r'^/(?P<id>\w+)/del/$', 'blog_del'),
)
