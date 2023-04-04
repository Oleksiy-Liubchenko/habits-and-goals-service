from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tracker.models import (
    Goal,
    GoalStage,
    Habit,
    Note,
    Commentary,
)


def index(request, pk):
    pass


class GoalListView(generic.ListView):
    model = Goal
    template_name = "goal/goal_list.html"
    context_object_name = "goal_list"


class GoalCreateView(generic.CreateView):
    model = Goal
    fields = "__all__"
    template_name = "goal/goal_form.html"
    success_url = reverse_lazy("tracker:goal-list")


class GoalDetailView(generic.DetailView):
    pass


class GoalStageCreateView(generic.CreateView):
    pass


class HabitListView(generic.ListView):
    pass


class HabitCreateView(generic.CreateView):
    pass


class HabitDetailView(generic.DetailView):
    pass


class NoteCreateView(generic.CreateView):
    pass


class CommentaryCreateView(generic.CreateView):
    pass
