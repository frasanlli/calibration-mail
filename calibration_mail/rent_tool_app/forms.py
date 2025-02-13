from django import forms
from .models import Device, Location

class Rent_device(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['is_available', 'location', 'is_calibrating']

    def __init__(self, *args, **kwargs):
        super(Rent_device, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()
