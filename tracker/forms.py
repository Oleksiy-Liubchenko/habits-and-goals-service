from django import forms
from django.forms import widgets
from tracker.models import Goal
from django.forms.widgets import DateInput


class GoalCreationForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'description', 'deadline']
        widgets = {
            'deadline': DateInput(attrs={'type': 'date'}),
        }
