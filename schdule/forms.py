from django import forms
from .models import task

class TaskForm(forms.ModelForm):
    class Meta:
        model = task
        fields = ['date', 'flexibility', 'departure_place', 'destination_place']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'flexibility': forms.NumberInput(attrs={'class': 'form-control'}),
            'departure_place': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'destination_place': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
