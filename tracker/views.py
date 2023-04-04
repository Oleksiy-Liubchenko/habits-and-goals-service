from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.forms import widgets

from tracker.forms import GoalCreationForm
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
    # widgets = {
    #     'deadline': widgets.DateInput(
    #         attrs={'type': 'datetime-local'},
    #         format='%Y-%m-%dT%H:%M'
    #     )
    # }


class GoalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Goal
    template_name = "goal/goal_form.html"
    success_url = reverse_lazy("tracker:goal-list")
    form_class = GoalCreationForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # widgets = {
    #     'deadline': widgets.DateInput(
    #         attrs={'type': 'datetime-local'},
    #         format='%Y-%m-%dT%H:%M'
    #     )
    # }

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
