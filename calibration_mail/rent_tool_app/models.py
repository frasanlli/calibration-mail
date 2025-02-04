from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from dateutil.relativedelta import relativedelta

class Location(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    # Set a custom primary key that combines city and country
    id = models.CharField(max_length=100, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate the ID in the format {city}_{country}
        self.id = f"{self.city}_{self.country}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city}, {self.country}"


class Device(models.Model):
    # Basic Device Information
    name = models.CharField(
        max_length=255,
        help_text="Name of the device"
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique serial number of the device"
    )
    manufacturer = models.CharField(
        max_length=255,
        help_text="Manufacturer of the device"
    )
    device_image = models.ImageField(
        blank=True,
        null=True,
    )
    model_number = models.CharField(
        max_length=100,
        help_text="Model number of the device"
    )
    warranty_expiry_date = models.DateField(
        help_text="Date when the device warranty expires"
    )

    # Calibration Information
    calibration_required = models.BooleanField(
        default=False,
        help_text="Whether the device requires calibration",
    )
    is_calibrating = models.BooleanField(
        default=False,
        help_text="Whether the device is currently being calibrated"
    )
    last_calibration_date = models.DateField(
        help_text="Date of the last calibration"
    )
    calibration_due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Next due date for calibration"
    )
    calibration_interval = models.PositiveIntegerField(
        default=24,
        validators=[MinValueValidator(1), MaxValueValidator(48)],
        help_text="Calibration interval in months"
    )

    # Control Information
    is_available = models.BooleanField(
        default=True,
        help_text="Whether the device is available to use it"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        help_text="Current location of the device",
        default="Valencia_Spain"
    )
    controlled_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User responsible for controlling the device"
    )

    # Additional Metadata
    created_at = models.DateTimeField(auto_now_add=True,
        help_text="Timestamp when the device was added to the system"
    )
    updated_at = models.DateTimeField(auto_now=True,
        help_text="Timestamp when the device was last updated"
    )

    def __str__(self):
        return f"{self.name} (SN: {self.serial_number})"

    def save(self, *args, **kwargs):
        # Automatically set the calibration due date based on the last calibration date and interval
        if self.last_calibration_date and self.calibration_interval:
            self.calibration_due_date = self.last_calibration_date + relativedelta(months=self.calibration_interval)
        super().save(*args, **kwargs)
