from django.contrib import admin
from django.urls import include, path
from polls.views import home

urlpatterns = [
    path('', home),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
