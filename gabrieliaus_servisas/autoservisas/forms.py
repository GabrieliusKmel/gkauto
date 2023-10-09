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