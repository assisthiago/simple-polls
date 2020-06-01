from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
