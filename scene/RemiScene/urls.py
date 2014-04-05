from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^scene/(?P<scene_id>\d+)$', 'RemiScene.scene_view.home', name='scene_home'),
)