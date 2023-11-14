from django.urls import path
from . import views

urlpatterns = [
  path('old', views.photo_wall, name='photo-wall'),
  path('name', views.get_name, name='get_name_url'),
  path('photo/<int:photo_id>', views.photo_view, name='photo_url'),
  path('deletephoto/<int:photo_id>', views.delete_view, name='delete_url'),

  path('', views.photo_wall_db_view, name='home_db_url'),
  path('add', views.new_post_view, name='add_db_url'),
  path('post/<str:post_id>', views.post_db_view, name='post_db_url'),
  path('delete/<str:pk>', views.DeletePostView.as_view(), name='delete_db_url'),
]
