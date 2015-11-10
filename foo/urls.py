from django.conf.urls import url
from foo import views

urlpatterns = [
    url(r'^foo/$', views.FooList.as_view()),
    url(r'^foo/(?P<pk>[0-9]+)/$', views.FooDetail.as_view()),
]
