from django.urls import path

from .views import get_tool, tools_state, update_device


urlpatterns = [
    path('', get_tool, name='get_tool'),
    path('tools_state', tools_state, name='tools_state'),
    path('update/<device_id>/', update_device, name='update_device'),
]

