from django.urls import path
from . import views

urlpatterns = [
  path('', views.photo_wall, name='photo-wall'),
  path('name', views.get_name, name='get_name_url'),
  path('photo/<int:photo_id>', views.photo_view, name='photo_url'),
  path('deletephoto/<int:photo_id>', views.delete_view, name='delete_url'),
]
