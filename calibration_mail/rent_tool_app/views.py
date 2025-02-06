from django.shortcuts import render
from .models import Device, Location

# Create your views here.

def get_tool (request):
    devices = Device.objects.all()
    #locations = Location.objects.all()

    return render(request, "get_tool/get_tool.html",
                  {"devices": devices})


def tools_state (request):

    #tools_state = Device.objects.all()
    return render(request, "tools_state/tools_state.html")