from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
import datetime
from tracker.models import Habit, Goal


class ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username='test_user',
            password='test_pass',
            first_name='Test',
            last_name='User'
        )

    def test_goal_format_str(self):
        format_ = Goal.objects.create(
            user=self.user,
            name="Test123",
            description="Description_Test",
            deadline=timezone.make_aware(
                datetime.datetime(2023, 3, 4)
            )
        )
        self.assertEqual(
            str(format_),
            format_.name
        )

    def test_habit_format_str(self):
        format_ = Habit.objects.create(
            user=self.user,
            name="Test123",
            description="Description_Test",
            month_goal="Test_month_goal"
        )
        self.assertEqual(
            str(format_),
            format_.name
        )
