# 明确绑定视图集到url
from snippets.views import SnippetViewSet, UserViewSet
from rest_framework import renderers
# 使用路由 使用Router类可以自动将资源与视图/链接联系起来
from rest_framework.routers import DefaultRouter
from snippets import views
from django.conf.urls import url, include

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delee': 'destroy'
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
},renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

'''
# 配置路由连接视图
from django.conf.urls import url, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
# api endpoint

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail')
])
'''


'''
# cbv写法 views.视图类.as_view()
urlpatterns = [
    url(r'^$', views.api_root)
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
]
# 给url添加格式后缀模式 为了能处理像http://example.com/api/items/4/.json一样的链接
urlpatterns = format_suffix_patterns(urlpatterns)
'''
