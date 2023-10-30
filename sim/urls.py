from django.urls import path
from . import views

urlpatterns = [
  path('', views.photo_wall, name='photo-wall'),
  path('name', views.get_name, name='get_name_url'),
]
