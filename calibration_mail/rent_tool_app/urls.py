from django.urls import path

from .views import get_tool, tools_state


urlpatterns = [
    path('', get_tool, name='get_tool'),
    path('tools_state', tools_state, name='tools_state'),
]

