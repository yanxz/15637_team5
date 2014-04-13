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
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)