from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils import timezone
import datetime

from tracker.forms import GoalNameSearchForm, HabitNameSearchForm
from tracker.views import GoalListView, HabitListView

from tracker.models import (
    Goal,
    GoalStage,
    Habit,
    Commentary,
    User)


GOAL_URL = reverse("tracker:goal-list")
HABIT_URL = reverse("tracker:habit-list")


class PublicGoalListViews(TestCase):
    def test_login_required(self):
        res = self.client.get(GOAL_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateGoalListViews(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test_user",
            password="TestPassword123"
        )
        self.factory = RequestFactory()
        self.client.force_login(self.user)

    def test_retrieve_goal(self):
        Goal.objects.create(
            user=self.user,
            name="Test_goal",
            description="Test_description",
            deadline=timezone.make_aware(
                datetime.datetime(2023, 3, 4)
            )
        )
        goal = Goal.objects.all()

        response = self.client.get(GOAL_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["goal_list"]),
            list(goal)
        )
        self.assertTemplateUsed(response, "goal/goal_list.html")

    def test_context_data_goal(self):
        response = self.client.get(
            "/goals/",
            {"name": "test_name"}
        )
        context = response.context_data
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            context["search_form"],
            GoalNameSearchForm
        )
        self.assertEqual(context["search_form"].initial["name"], "test_name")

    def test_queryset_goal(self):
        Goal.objects.create(
            user=self.user,
            name="Test_goal",
            description="Test_description",
            deadline=timezone.make_aware(
                datetime.datetime(2023, 3, 4)
            )
        )

        url = reverse("tracker:goal-list")
        request = self.factory.get(url, {"name": "test"})
        request.user = self.user

        response = GoalListView.as_view()(request)

        self.assertQuerysetEqual(
            list(response.context_data["goal_list"]),
            list(Goal.objects.filter(name__icontains="test"))
        )


class TestGoalAndGoalStageToggleStatus(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Test_user",
            password="Test_pass"
        )
        self.goal = Goal.objects.create(
            user=self.user,
            name="Test_Goal",
            description="Test_Description",
            deadline=timezone.make_aware(
                datetime.datetime(2023, 3, 4)
            )
        )
        self.goal_stage = GoalStage.objects.create(
            stage_name="Test Goal Stage",
            description="Test Goal Stage Description",
            goal=self.goal
        )

    def test_goal_toggle_status(self):
        self.client.login(username="Test_user", password="Test_pass")

        response = self.client.post(
            reverse(
                "tracker:goal-update-status", args=[self.goal.pk]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse(
                "tracker:goal-detail", args=[self.goal.pk]
            )
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.status, "completed")

    def test_goal_toggle_status_abandoned(self):
        self.client.login(username="Test_user", password="Test_pass")

        response = self.client.post(reverse(
            "tracker:goal-update-status-abandoned", args=[self.goal.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse(
                "tracker:goal-detail", args=[self.goal.pk]
            )
        )
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.status, "abandoned")

    def test_goal_stage_toggle_status(self):
        self.client.login(username="Test_user", password="Test_pass")

        response = self.client.post(
            reverse(
                "tracker:goal-update-stage-status",
                args=[self.goal.pk, self.goal_stage.pk]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(
            "tracker:goal-detail", args=[self.goal.pk]
        ))
        self.goal_stage.refresh_from_db()
        self.assertEqual(self.goal_stage.status, "completed")

    def test_goal_stage_toggle_status_abandoned(self):
        self.client.login(username="Test_user", password="Test_pass")

        response = self.client.post(
            reverse(
                "tracker:goal-update-stage-status-abandoned",
                args=[self.goal.pk, self.goal_stage.pk]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(
            "tracker:goal-detail", args=[self.goal.pk]
        ))
        self.goal_stage.refresh_from_db()
        self.assertEqual(self.goal_stage.status, "abandoned")


class PublicHabitListViews(TestCase):
    def test_login_required(self):
        res = self.client.get(HABIT_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateHabitListViews(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test_user",
            password="TestPassword123"
        )
        self.factory = RequestFactory()
        self.client.force_login(self.user)

    def test_retrieve_habit(self):
        Habit.objects.create(
            user=self.user,
            name="Test_habit",
        )
        habit = Habit.objects.all()

        response = self.client.get(HABIT_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            list(response.context["habit_list"]),
            list(habit)
        )
        self.assertTemplateUsed(response, "habit/habit_list.html")

    def test_context_data_habit(self):
        response = self.client.get(
            "/habits/",
            {"name": "test_name"}
        )
        context = response.context_data
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            context["search_form"],
            HabitNameSearchForm
        )
        self.assertEqual(context["search_form"].initial["name"], "test_name")

    def test_queryset_habit(self):
        Habit.objects.create(
            user=self.user,
            name="Test_habit",
        )

        url = reverse("tracker:habit-list")
        request = self.factory.get(url, {"name": "test"})
        request.user = self.user

        response = HabitListView.as_view()(request)

        self.assertQuerysetEqual(
            list(response.context_data["habit_list"]),
            list(Habit.objects.filter(name__icontains="test"))
        )


class TestCommentaryHabitCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Test_user", password="Test_password"
        )
        self.habit = Habit.objects.create(name="Test_habit", user=self.user)
        self.goal = Goal.objects.create(
            name="Test_goal",
            user=self.user,
            deadline=timezone.make_aware(
                datetime.datetime(2023, 3, 4)
            )
        )

    def test_habit_commentary_create_view_success(self):
        self.client.login(username="Test_user", password="Test_password")
        form_data = {
            "text": "This is a test commentary."
        }
        response = self.client.post(
            reverse(
                "tracker:habit-commentary-create", kwargs={"pk": self.habit.pk}
            ),
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse("tracker:habit-detail", kwargs={"pk": self.habit.pk})
        )

        commentary = Commentary.objects.first()

        self.assertEqual(commentary.text, "This is a test commentary.")
        self.assertEqual(commentary.user, self.user)
        self.assertEqual(commentary.habits.first(), self.habit)

    def test_goal_commentary_create_view_success(self):
        self.client.login(username="Test_user", password="Test_password")
        form_data = {
            "text": "This is a test commentary."
        }
        response = self.client.post(
            reverse(
                "tracker:goal-commentary-create", kwargs={"pk": self.habit.pk}
            ),
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse("tracker:goal-detail", kwargs={"pk": self.goal.pk})
        )

        commentary = Commentary.objects.first()

        self.assertEqual(commentary.text, "This is a test commentary.")
        self.assertEqual(commentary.user, self.user)
        self.assertEqual(commentary.goals.first(), self.goal)


class HabitDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Test_user",
            password="Test_pass"
        )
        self.habit = Habit.objects.create(
            name="Test Habit",
            description="This is a test habit",
            user=self.user
        )
        self.url = reverse(
            "tracker:habit-detail", kwargs={"pk": self.habit.pk}
        )

    def test_habit_view_requires_login(self):

        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("login") + f"?next={self.url}"
        )

    def test_view_displays_habit_details(self):
        self.client.login(username="Test_user", password="Test_pass")
        response = self.client.get(self.url)
        self.assertContains(response, "Test Habit")
        self.assertContains(response, "This is a test habit")


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("tracker:index")
        self.user = User.objects.create_user(
            username="Test_user", password="Test_pass"
        )

    def test_view_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, reverse("login") + f"?next={self.url}"
        )
