from django.conf.urls import url
from foo import views

urlpatterns = [
    url(r'^foo/$', views.foo_list),
    url(r'^foo/(?P<pk>[0-9]+)/$', views.foo_detail),
]
