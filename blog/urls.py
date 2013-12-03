from django.conf.urls import *

urlpatterns = patterns(('blog.views'),
    url(r'^$', 'blog_list', name = 'bloglist'),
    url(r'^blog/(?P<id>\d+)/$', 'blog_show', name = 'detailblog'),
)
