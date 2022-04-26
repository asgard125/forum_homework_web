from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

from mysite import settings
from ml_forum.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ml_forum.urls')),
    path('captcha/', include('captcha.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
handler403 = pageForbidden