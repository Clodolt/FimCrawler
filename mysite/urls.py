from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('journals/', views.journals, name ='journals'),
    path('crawls/', views.crawls, name ='crawls'),
    path('mails/', views.mails, name ='mails'),
    path('list/', views.journal_list, name ='list'),
]