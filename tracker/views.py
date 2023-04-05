from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.forms import widgets

from tracker.forms import GoalCreationForm, GoalCreationStageForm, GoalCommentaryForm, HabitCreationForm, \
    HabitCommentaryForm
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
        context['goal_commentaries'] = self.object.commentaries.all()
        return context


class GoalStageCreateView(generic.CreateView):
    model = GoalStage
    form_class = GoalCreationStageForm
    template_name = "goal/goalstage_form.html"

    def form_valid(self, form):
        form.instance.goal_id = self.kwargs["goal_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tracker:goal-detail", kwargs={"pk": self.kwargs["goal_id"]})


class HabitListView(generic.ListView):
    model = Habit
    template_name = "habit/habit_list.html"


class HabitCreateView(generic.CreateView):
    model = Habit
    template_name = "habit/habit_form.html"
    success_url = reverse_lazy("tracker:habit-list")
    form_class = HabitCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HabitDetailView(generic.DetailView):
    model = Habit
    template_name = "habit/habit_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["habit_commentaries"] = self.object.commentaries.all()
        return context


class NoteCreateView(generic.CreateView):
    pass


class CommentaryGoalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Commentary
    form_class = GoalCommentaryForm
    template_name = "commentary_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goal_id"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        goal = Goal.objects.get(pk=self.kwargs["pk"])
        commentary = form.save(commit=False)
        commentary.user = self.request.user
        commentary.save()
        commentary.goals.add(goal)
        commentary.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tracker:goal-detail", kwargs={"pk": self.kwargs["pk"]})


class CommentaryHabitCreateView(generic.CreateView):
    model = Commentary
    form_class = HabitCommentaryForm
    template_name = "habit/habit_commentary_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["habit_id"] = self.kwargs["pk"]
        return context

    def form_valid(self, form):
        habit = Habit.objects.get(pk=self.kwargs["pk"])
        commentary = form.save(commit=False)
        commentary.user = self.request.user
        commentary.save()
        commentary.habits.add(habit)
        commentary.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tracker:habit-detail", kwargs={"pk": self.kwargs["pk"]})
