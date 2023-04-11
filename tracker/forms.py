from django import forms
from django.forms import widgets
from tracker.models import Goal, GoalStage, Commentary, Habit, HabitDayCompletion
from django.forms.widgets import DateInput


class GoalNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by goal name"
            }
        )
    )


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


# GoalCommentaryForm
class GoalCommentaryForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["text"]


class HabitCreationForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "description", "month_goal"]


class HabitCommentaryForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["text"]


class HabitDayCompletionForm(forms.ModelForm):
    class Meta:
        model = HabitDayCompletion
        fields = ["status"]
        widgets = {
            "status": forms.RadioSelect(),
        }
