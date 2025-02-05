from django.shortcuts import render
from .models import Device

# Create your views here.

def get_tool (request):

    #get_tool = Device.objects.all()
    return render(request, "get_tool/get_tool.html")

def tools_state (request):

    #tools_state = Device.objects.all()
    return render(request, "tools_state/tools_state.html")