from django.conf.urls import url
from boards import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
]
