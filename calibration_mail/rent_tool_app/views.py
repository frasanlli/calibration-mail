from django.shortcuts import render
from .models import Device, Location

# Create your views here.

def get_tool (request):
    devices = Device.objects.all()
    #locations = Location.objects.all()

    return render(request, "get_tool/get_tool.html",
                  {"devices": devices})


def tools_state (request):

    tools_need_calibration = Device.objects.filter(calibration_required = True).values()
    tools_are_calibrating = Device.objects.filter(is_calibrating = True).values()
    tools_not_factory = Device.objects.exclude(location = "Valencia_Spain").values()
    tools_not_available = Device.objects.filter(is_available = False).values()
    return render(request,
                  "tools_state/tools_state.html",
                  {"tools_need_calibration": tools_need_calibration,
                  "tools_are_calibrating": tools_are_calibrating,
                  "tools_not_factory": tools_not_factory,
                  "tools_not_available": tools_not_available})