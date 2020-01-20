from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from mysite.core import views as core_views
import mysite.settings as settings
from django.views.static import serve

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/password/$', core_views.password, name='password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),
    url(r'^text/', core_views.shashank, name='shashank'),
    url(r'^newtext/', core_views.newtext, name='newtext'),
    url(r'^mytest/', core_views.getUsername, name='getUsername'),
    # url(r'^media/(?P.*)$', serve ,{'document_root': settings.MEDIA_ROOT}),
]