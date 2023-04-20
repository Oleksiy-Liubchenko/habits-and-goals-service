import datetime

from django import forms
from django.test import TestCase
from django.utils import timezone

from tracker.forms import (
    GoalNameSearchForm,
    GoalCreationForm,
    GoalCreationStageForm,
    GoalCommentaryForm,
    HabitNameSearchForm,
    HabitCreationForm,
    HabitCommentaryForm,
)


class FormsTest(TestCase):
    def test_goal_search_by_name_form_widget(self):
        form = GoalNameSearchForm()

        self.assertIsInstance(
            form.fields["name"].widget, forms.TextInput
        )

    def test_goal_creation_form_is_valid(self):
        deadline = timezone.make_aware(
            datetime.datetime(2023, 3, 4)
        )
        data = {
            "name": "Test_name",
            "description": "Test_description",
            "deadline": deadline
        }

        form = GoalCreationForm(data=data)

        self.assertTrue(form.is_valid())

    def test_goal_creation_form_without_deadline(self):
        data = {
            "name": "Test_name",
            "description": "Test_description",
            "deadline": ""
        }

        form = GoalCreationForm(data=data)

        self.assertFalse(form.is_valid())

    def test_goal_stage_creation_form_is_valid(self):
        deadline = timezone.make_aware(
            datetime.datetime(2023, 3, 4)
        )
        data = {
            "stage_name": "Test_name",
            "description": "Test_description",
            "deadline": deadline
        }

        form = GoalCreationStageForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_goal_commentary_form_is_valid(self):
        data = {"text": "Test commentary"}
        form = GoalCommentaryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_goal_commentary_form_blank_text(self):
        data = {"text": ""}
        form = GoalCommentaryForm(data=data)
        self.assertFalse(form.is_valid())

    def test_habit_search_by_name_form_widget(self):
        form = HabitNameSearchForm()

        self.assertIsInstance(
            form.fields["name"].widget, forms.TextInput
        )

    def test_habit_creation_form_is_valid(self):
        data = {
            "name": "Test_name",
            "description": "Test_description",
            "month_goal": "Test_month_goal"
        }

        form = HabitCreationForm(data=data)

        self.assertTrue(form.is_valid())

    def test_habit_commentary_form_is_valid(self):
        data = {"text": "Test commentary"}
        form = HabitCommentaryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_habit_commentary_form_blank_text(self):
        data = {"text": ""}
        form = HabitCommentaryForm(data=data)
        self.assertFalse(form.is_valid())
