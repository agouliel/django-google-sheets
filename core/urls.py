from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('sim.urls')),
    path('', include('pages.urls')),
    path('media/<str:path>', serve, {'document_root': settings.MEDIA_ROOT,}),
]

# the below should be included in settings as well
urlpatterns = [path('alexgram/', include(urlpatterns))]
