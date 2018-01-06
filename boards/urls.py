from django.conf.urls import url
from boards import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    url(r'^(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)$',
        views.topic_posts, name='topic_posts'),
    url(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$',
        views.reply_topic, name='reply_topic'),
    url(r'^(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/post/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
]
