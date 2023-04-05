from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.forms import widgets

from tracker.forms import GoalCreationForm, GoalCreationStageForm
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


class GoalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Goal
    template_name = "goal/goal_form.html"
    success_url = reverse_lazy("tracker:goal-list")
    form_class = GoalCreationForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GoalDetailView(generic.DetailView):
    model = Goal
    template_name = "goal/goal_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal_stages'] = self.object.stages.all()
        return context


class GoalStageCreateView(generic.CreateView):
    model = GoalStage
    form_class = GoalCreationStageForm
    #success_url = reverse_lazy("tracker:goal-detail")
    template_name = "goal/goalstage_form.html"

    def form_valid(self, form):
        form.instance.goal_id = self.kwargs["goal_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tracker:goal-detail", kwargs={"pk": self.kwargs["goal_id"]})


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
