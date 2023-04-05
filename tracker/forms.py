from django import forms
from django.forms import widgets
from tracker.models import Goal, GoalStage
from django.forms.widgets import DateInput


class GoalCreationForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'description', 'deadline']
        widgets = {
            'deadline': DateInput(attrs={'type': 'date'}),
        }


class GoalCreationStageForm(forms.ModelForm):
    class Meta:
        model = GoalStage
        fields = ['stage_name', 'description', 'deadline']
        widgets = {
            'deadline': DateInput(attrs={'type': 'date'})
        }
