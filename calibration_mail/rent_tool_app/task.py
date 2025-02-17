from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Device

@shared_task
def send_daily_device_report():
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
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list = [settings.NOTIFY_EMAIL],
    )
