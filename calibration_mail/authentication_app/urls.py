from django.urls import path

from .views import log_out, log_in


urlpatterns = [
    path('', log_in, name='log_in'),
    path('log_out', log_out, name='log_out'),
]

