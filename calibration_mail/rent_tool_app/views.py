from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from .forms import Rent_device, Upload_file_form
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
            if device_instance.is_available != True and device_instance.is_calibrating != True:
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

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = Upload_file_form(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Read the Excel file using xlrd as the engine
                df = pd.read_excel(file, engine='xlrd')

                # Iterate over rows and create Device instances
                for index, row in df.iterrows():
                    Device.objects.create(
                        name=row['name'],
                        serial_number=row['serial_number'],
                        last_calibration_date=row['calibration_date']
                        # Other fields will use their default values
                    )

                messages.success(request, "Devices imported successfully!")
                return redirect('upload_file')

            except Exception as e:
                messages.error(request, f"Error importing devices: {str(e)}")
    else:
        form = Upload_file_form()

    return render(request, 'upload_file/upload_file.html', {'form': form})
"""def import_devices_from_excel(file):
    df = pd.read_excel(file)
    for index, row in df.iterrows():
        Device.objects.create(
            name=row['Name'],
            serial_number=row['Serial Number'],
            calibration_date=row['Calibration Date']
        )

@login_required
def upload_file(request):
    if request.user.is_superuser:

        if request.method == 'POST':
            form = Upload_file_form(request.POST, request.FILES)
            if form.is_valid():
                try:
                    import_devices_from_excel(request.FILES['file'])
                    messages.success(request, 'Devices imported successfully!')
                except Exception as e:
                    messages.error(request, f'Error importing devices: {str(e)}')
                return redirect('upload_file')
        else:
            form = Upload_file_form()

        return render(request, 'upload_file/upload_file.html', {'form': form})"""
