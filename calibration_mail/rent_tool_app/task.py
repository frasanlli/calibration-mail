from django.core.mail import send_mail
from django.conf import settings
from .models import Device

def send_daily_device_report():
    # Devices that require calibration and are not calibrating
    devices_need_calibration = Device.objects.filter(
        calibration_required = True,
        is_calibrating = False
    )
    # Devices that are currently calibrating
    devices_calibrating = Device.objects.filter(is_calibrating = True)

    #Devices that are out of the factory non-case sensitive
    devices_out = Device.objects.exclude(location__iexact="factory")

    # Prepare email content
    subject = "Daily Device Report"
    message = "Devices that require calibration and are not calibrating:\n"
    for device in devices_need_calibration:
        message += f"- {device.name} (SN: {device.serial_number})\n"

    message += "\nDevices that are currently calibrating:\n"
    for device in devices_calibrating:
        message += f"- {device.name} (SN: {device.serial_number})\n"

    message += "\nDevices that are currently out of the factory:\n"
    for device in devices_out:
        message += f"- {device.name} (SN: {device.serial_number}, Location: {device.location})\n"

    # Send email
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["admin@example.com"],  # Replace with your email list
    )