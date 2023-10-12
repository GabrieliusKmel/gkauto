from django import forms
from . import models


class PartServiceReviewForm(forms.ModelForm):
    class Meta:
        model = models.PartServiceReview
        fields = ('content', 'partservice', 'reviewer')
        widgets = {
            'partservice': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }
        labels = {
            'content': '',
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ['car_model', 'plate', 'vin', 'color']
        labels = {
            'car_model': 'Mašinos modelis',
            'plate': 'Numeris',
            'vin': 'VIN',
            'color': 'Spalva',
        }

class PartServiceForm(forms.ModelForm):
    part_service = forms.ModelChoiceField(
        queryset=models.PartService.objects.all(),
        label='Pasirinkite paslaugą',
    )

    class Meta:
        model = models.CarPartService
        fields = ['part_service', 'problem'] 
        labels = {
            'problem': 'Aprašykite problemą',
        }