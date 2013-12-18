from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(('blog.views'),
    url(r'^blog/$', 'blog_list', name = 'bloglist'),
    url(r'^blog/blog/(?P<id>\d+)/$', 'blog_show', name = 'detailblog'),
    url(r'^search$', 'search', name = 'search'),
    url(r'^blog/tag/(?P<id>\d+)/$', 'search_tag', name='searchtag'),
    url(r'^blog/add/$', 'blog_add', name='addblog'),
    url(r'^blog/(?P<id>\d+)/update/$', 'blog_update', name='updateblog'),
    url(r'^blog/(?P<id>\w+)/del/$', 'blog_del', name='delblog'),
    url(r'^login/$', 'login', name = 'login'),
    url(r'^logout/$', 'logout', name = 'logout'),
)

urlpatterns += patterns((''),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}  
    ),
)

