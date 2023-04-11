from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.forms import widgets

from tracker.forms import GoalCreationForm, GoalCreationStageForm, GoalCommentaryForm, HabitCreationForm, \
    HabitCommentaryForm, HabitDayCompletionForm
from tracker.models import (
    Goal,
    GoalStage,
    Habit,
    Note,
    Commentary, HabitDayCompletion, User
)


def index(request):
    context = {}

    return render(request, "index.html", context=context)


class GoalListView(generic.ListView):
    model = Goal
    template_name = "goal/goal_list.html"
    context_object_name = "goal_list"
    paginate_by = 5


class GoalActiveListView(generic.ListView):
    model = Goal
    template_name = "goal/goal_list_active.html"
    context_object_name = "goal_list_active"
    paginate_by = 5
    queryset = Goal.objects.filter(status="active")


class GoalCompletedListView(generic.ListView):
    model = Goal
    template_name = "goal/goal_list_completed.html"
    context_object_name = "goal_list_completed"
    paginate_by = 5
    queryset = Goal.objects.filter(status="completed")


class GoalAbandonedListView(generic.ListView):
    model = Goal
    template_name = "goal/goal_list_abandoned.html"
    context_object_name = "goal_list_abandoned"
    paginate_by = 5
    queryset = Goal.objects.filter(status="abandoned")


class GoalDeleteView(generic.DeleteView):
    model = Goal
    template_name = "goal/goal_confirm_delete.html"
    success_url = reverse_lazy("tracker:goal-list")


class GoalUpdateView(generic.UpdateView):
    model = Goal
    fields = "__all__"
    template_name = "goal/goal_form.html"

    def get_success_url(self):
        return reverse("tracker:goal-detail", kwargs={"pk": self.kwargs["pk"]})

# class GoalUpdateStatus(generic.UpdateView):
#     model = Goal
#     fields = ["status",]
#     template_name = goa


# add login required
def goal_toggle_status(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if goal.status == "active":
        goal.status = "completed"
    else:
        goal.status = "active"
    goal.save()
    return HttpResponseRedirect(reverse_lazy("tracker:goal-detail", args=[pk]))


# add login required
def goal_toggle_status_abandoned(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if goal.status == "abandoned":
        goal.status = "active"
    else:
        goal.status = "abandoned"
    goal.save()

    return HttpResponseRedirect(reverse_lazy("tracker:goal-detail", args=[pk]))


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


class GoalStageDeleteView(generic.DeleteView):
    model = GoalStage
    template_name = "goal/goalstage_confirm_delete.html"
    success_url = reverse_lazy("tracker:goal-list")

    def get_success_url(self):
        return reverse("tracker:goal-detail", kwargs={"pk": self.kwargs["goal_id"]})


class GoalStageUpdateView(generic.UpdateView):
    model = GoalStage
    fields = "__all__"
    template_name = "goal/goalstage_form.html"
    success_url = reverse_lazy("tracker:goal-list")

    def get_success_url(self):
        return reverse("tracker:goal-detail", kwargs={"pk": self.kwargs["goal_id"]})


class HabitListView(generic.ListView):
    model = Habit
    template_name = "habit/habit_list.html"
    paginate_by = 5


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
        context["form"] = HabitDayCompletionForm()
        total_days = (date.today() - self.object.created_at.date()).days
        context["total_days"] = total_days if total_days > 0 else 1
        context["completed_days"] = self.object.habit_completions.filter(status="completed").count()
        # --- if you will not use hide status if completed - delete comp.status.today
        context["completion_status_today"] = self.object.habit_completions.filter(complete_date=date.today()).first()
        # ---
        context["not_completed_days"] = self.object.habit_completions.filter(status="not_completed").count()
        context["ignored_days"] = context["total_days"] - (context["completed_days"] + context["not_completed_days"])
        context["update_completion_form"] = HabitDayCompletionForm(instance=context["completion_status_today"]) if context["completion_status_today"] else None
        context["progress_percent"] = 100 * round((context["completed_days"] / context["total_days"]), 2) if context["total_days"] else 0
        return context

    def post(self, request, *args, **kwargs):
        habit = self.get_object()
        form = HabitDayCompletionForm(request.POST)
        if form.is_valid():
            completion = form.save(commit=False)
            completion.user = request.user
            completion.habit = habit
            completion.complete_date = date.today()
            completion.save()
            messages.success(
                request,
                f"Habit '{habit.name}' marked as '{completion.get_status_display()}' for today."
            )
        return redirect('tracker:habit-detail', pk=habit.pk)

# def habit_detail(request, pk):
#     habit = get_object_or_404(Habit, pk=pk)
#     if request.method == 'POST':
#         form = HabitDayCompletionForm(request.POST)
#         if form.is_valid():
#             completion = HabitDayCompletion.objects.create(
#                 user=request.user,
#                 habit=habit,
#                 complete_date=date.today(),
#                 status=form.cleaned_data['status'],
#             )
#             messages.success(request, f"Habit '{habit.name}' marked as '{completion.get_status_display()}' for today.")
#             return redirect('habit_detail', pk=habit.pk)
#     else:
#         form = HabitDayCompletionForm()
#     context = {
#         'habit': habit,
#         'form': form,
#     }
#     return render(request, 'habit/habit_detail.html', context)

# trying to update status for each day or only last status:
# ---------------
# class HabitDayCompletionUpdateView(generic.UpdateView):
#     model = HabitDayCompletion
#     fields = ["habit", "status"]
#     template_name = "habit/habit_day_completion_form.html"
#
#     # def get_queryset(self):
#     #     return HabitDayCompletion.objects.filter(
#     #         user=self.request.user,
#     #         habit_id=self.kwargs["pk"]
#     #     )
#
#     def get_success_url(self):
#         return reverse("tracker:habit-detail", kwargs={"pk": self.kwargs["pk"]})

# ---------------


class NoteCreateView(generic.CreateView):
    pass


class CommentaryGoalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Commentary
    form_class = GoalCommentaryForm
    template_name = "goal/goal_commentary_form.html"

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
