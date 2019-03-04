from django.conf.urls import url
# 从当前目录下导入了 views 模块
from . import views

app_name = 'blog'
# 把网址和处理函数的关系写在了 urlpatterns 列表里，绑定网址与处理函数
# 绑定关系的写法是：把网址和对应的处理函数作为参数传递给url函数，
# 第一个参数是网址　，第二个参数是处理函数（视图函数），最后一个参数是作为处理函数的别名，以后会用到
# 这里网址的匹配是用正则表达式写的，Django 会用这个正则表达式去匹配用户实际输入的网址，
# 如果匹配成功，就会调用其后面的视图函数做相应的处理。
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'), # 把相关的 URL 和视图函数绑定在一起
	url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
	url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
]