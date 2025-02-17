from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import Rent_device
from .models import Device, Location

# Create your views here.
@login_required
def get_tool (request):
    devices = Device.objects.all()

    return render(request, "get_tool/get_tool.html",
                  {"devices": devices})

@login_required
def tools_state (request):
    tools_need_calibration = Device.objects.filter(calibration_required = True).all()
    tools_are_calibrating = Device.objects.filter(is_calibrating = True).all()
    tools_not_factory = Device.objects.exclude(location = "Valencia_Spain").all()
    tools_not_available = Device.objects.filter(is_available = False, location = "Valencia_Spain").all()
    return render(request,
                  "tools_state/tools_state.html",
                  {"tools_need_calibration": tools_need_calibration,
                  "tools_are_calibrating": tools_are_calibrating,
                  "tools_not_factory": tools_not_factory,
                  "tools_not_available": tools_not_available})

@login_required
def update_device(request, device_id):
    instance = get_object_or_404(Device, pk=device_id)

    if request.method == 'POST':
        form = Rent_device(request.POST, instance=instance)
        if form.is_valid():
            device_instance = form.save(commit=False)
            if device_instance.is_available != True:
                device_instance.controlled_by = request.user  # Set the user to the currently logged-in user
            else:
                device_instance.controlled_by = None
            device_instance.save()
            return tools_state(request)
    else:
        form = Rent_device(instance=instance)

    return render(request, 'rent_tool/rent_tool.html', {'form': form, 'device': instance})

@login_required
def send_report():
    # Devices that require calibration and are not calibrating
    devices_need_calibration = Device.objects.filter(
        calibration_required = True,
        is_calibrating = False
    )
    # Devices that are currently calibrating
    devices_calibrating = Device.objects.filter(is_calibrating = True)

    #Devices that are out of the factory non-case sensitive
    devices_out = Device.objects.exclude(location__exact="Valencia, Spain")

    # Prepare email content
    subject: str = "Daily Device Report"
    message: str = ""
    if devices_need_calibration:
        message += "Devices that require calibration and are not calibrating:\n"
        for device in devices_need_calibration:
            message += f"- {device.name} (SN: {device.serial_number})\n"

    if devices_calibrating:
        message += "\nDevices that are currently calibrating:\n"
        for device in devices_calibrating:
            message += f"- {device.name} (SN: {device.serial_number})\n"

    if devices_out:
        message += "\nDevices that are currently out of the factory:\n"
        for device in devices_out:
            message += f"- {device.name} (SN: {device.serial_number}, Location: {device.location}), User: {device.controlled_by}\n"

    # Send email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list = [settings.NOTIFY_EMAIL],
        )

        return redirect("tools_state?valid.html")

    except:
        return redirect("tools_state?error.html")
