from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import get_tool, tools_state, update_device, send_report, upload_file


urlpatterns = [
    path('get_tool', get_tool, name='get_tool'),
    path('tools_state', tools_state, name='tools_state'),
    path('update/<device_id>/', update_device, name='update_device'),
    path('send_report', send_report, name='send_report'),
    path('upload_file', upload_file, name='upload_file'),
]
urlpatterns+=static(settings.MEDIA_URL,
                    document_root = settings.MEDIA_ROOT)
