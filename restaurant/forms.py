from django import forms
from django.utils import timezone
from .models import Reservation, Order, OrderItem
from .services import ReservationService

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'contact', 'table', 'reservation_time', 'guest_count']
        widgets = {
            'reservation_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'block w-full rounded-none border-gray-300 bg-gray-50/50 py-3 px-4 text-sm shadow-sm focus:border-primary focus:ring-primary focus:bg-white transition-colors'}),
            'customer_name': forms.TextInput(attrs={'class': 'block w-full rounded-none border-gray-300 bg-gray-50/50 py-3 px-4 text-sm shadow-sm focus:border-primary focus:ring-primary focus:bg-white transition-colors', 'placeholder': 'Jane Doe'}),
            'contact': forms.TextInput(attrs={'class': 'block w-full rounded-none border-gray-300 bg-gray-50/50 py-3 px-4 text-sm shadow-sm focus:border-primary focus:ring-primary focus:bg-white transition-colors', 'placeholder': '+1 (555) 000-0000'}),
            'table': forms.Select(attrs={'class': 'block w-full rounded-none border-gray-300 bg-gray-50/50 py-3 px-4 text-sm shadow-sm focus:border-primary focus:ring-primary focus:bg-white transition-colors'}),
            'guest_count': forms.NumberInput(attrs={'class': 'block w-full rounded-none border-gray-300 bg-gray-50/50 py-3 px-4 text-sm shadow-sm focus:border-primary focus:ring-primary focus:bg-white transition-colors', 'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        reservation_time = cleaned_data.get('reservation_time')
        guest_count = cleaned_data.get('guest_count')

        if table and reservation_time:
            if reservation_time < timezone.now():
                raise forms.ValidationError("Reservation time cannot be in the past.")

            if guest_count and guest_count > table.capacity:
                raise forms.ValidationError(f"Guest count exceeds table capacity ({table.capacity}).")

            if not ReservationService.check_availability(table, reservation_time):
                raise forms.ValidationError("The selected table is not available at this time. Please choose another table or time.")

        return cleaned_data
