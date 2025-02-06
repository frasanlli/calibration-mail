from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import log_out, log_in


urlpatterns = [
    path('', log_in, name='log_in'),
    path('log_out', log_out, name='log_out'),
]

urlpatterns+=static(settings.MEDIA_URL,
                    document_root = settings.MEDIA_ROOT)