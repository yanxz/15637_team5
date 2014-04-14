from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
urlpatterns = patterns('',
    url(r'^scene/(?P<scene_id>\d+)$', 'RemiScene.scene_view.home', name='scene_home'),
    url(r'^$','RemiScene.home_view.home',name='home'),
    url(r'^home$','RemiScene.home_view.home',name='home'),
    url(r'^login$','RemiScene.login_view.my_login',name='login'),
    url(r'^register$','RemiScene.login_view.register',name='register'),
    url(r'^confirm/(?P<email>[^/]*)/(?P<token>[^/]*)', 'RemiScene.login_view.confirm', name='confirm'),
    url(r'^ts$','RemiScene.login_view.test'),
    url(r'^map$', 'RemiScene.map_view.home', name='map_home'),
    url(r'^scene/create$', 'RemiScene.home_view.manage_scene_create', name='create_scene'),
    url(r'^scene/add_scene$', 'RemiScene.home_view.add_scene', name='add_scene'),
    url(r'^search_people$', 'RemiScene.home_view.search_people', name='search_people'),
    url(r'^add_friend/(?P<userid>\d+)$', 'RemiScene.home_view.add_friend', name='add_friend'),
    url(r'^edit_person_scene/(?P<id>\d+)$','RemiScene.login_view.edit_person_scene',name='edit_person_scene'),
    url(r'^get_photo/(?P<username>[^/]*)/(?P<id>\d+)/(?P<type>\d)','RemiScene.login_view.get_photo',name='get_photo'),
    url(r'^get_music/(?P<username>[^/]*)/(?P<id>\d+)/(?P<type>\d)','RemiScene.login_view.get_music',name='get_music'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)