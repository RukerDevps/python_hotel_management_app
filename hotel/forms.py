from django import forms
from .models import Booking

class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)





class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
