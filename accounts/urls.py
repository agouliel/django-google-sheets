from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('register/', SignupPageView.as_view(), name='signup_db_url'),
]