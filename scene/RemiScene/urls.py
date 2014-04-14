from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
urlpatterns = patterns('',
    url(r'^scene/(?P<scene_id>\d+)$', 'RemiScene.scene_view.home', name='scene_home'),
    url(r'^$','RemiScene.home_view.home',name='home'),
    url(r'^login$','RemiScene.login_view.my_login',name='login'),
    url(r'^register$','RemiScene.login_view.register',name='register'),
    url(r'^confirm/(?P<email>[^/]*)/(?P<token>[^/]*)', 'RemiScene.login_view.confirm', name='confirm'),
    url(r'^ts$','RemiScene.login_view.test'),
    url(r'^map$', 'RemiScene.map_view.home', name='map_home'),
    url(r'^scene/create$', 'RemiScene.home_view.manage_scene_create', name='create_scene'),
    url(r'^scene/add_scene$', 'RemiScene.home_view.add_scene', name='add_scene'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)