from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tracker.admin import GoalAdmin, GoalStageInline
from tracker.models import Goal


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
            username="Test_user",
            password="driver12345",
        )
        self.client.force_login(self.user)

    def test_user_add_additional_fields(self):
        url = reverse("admin:tracker_user_add")
        res = self.client.get(url)

        self.assertContains(res, "first_name")
        self.assertContains(res, "last_name")

    def test_goal_stage_inline(self):
        goal_admin = GoalAdmin(Goal, admin.site)

        self.assertIn(GoalStageInline, goal_admin.inlines)
