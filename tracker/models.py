from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("abandoned", "Abandoned")
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )


class GoalStage(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='stages')
    stage_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("abandoned", "Abandoned")
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    month_goal = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitDayCompletion(models.Model):
    STATUS_CHOICE = [
        ("completed", "Competed"),
        ("not_completed", "Not Competed")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habit_completions')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_completions')

    complete_date = models.DateField()
    status = models.CharField(
        max_length=13,
        choices=STATUS_CHOICE,
        default="not_completed"
    )

    def __str__(self):
        return self.habit


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField()
    goals = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='notes')
    habits = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Commentary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    goals = models.ManyToManyField(Goal, related_name='commentaries')
    habits = models.ManyToManyField(Habit, related_name='commentaries')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
