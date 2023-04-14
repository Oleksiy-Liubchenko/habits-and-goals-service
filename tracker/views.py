from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from tracker.forms import (
    GoalCreationForm,
    GoalCreationStageForm,
    GoalCommentaryForm,
    HabitCreationForm,
    HabitCommentaryForm,
    HabitDayCompletionForm,
    GoalNameSearchForm,
    HabitNameSearchForm
)
from tracker.models import (
    Goal,
    GoalStage,
    Habit,
    Commentary
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    user = request.user
    active_goals_number = Goal.objects.filter(
        status="active", user=user
    ).count()
    completed_goals_number = Goal.objects.filter(
        status="completed", user=user
    ).count()
    abandoned_goals_number = Goal.objects.filter(
        status="abandoned", user=user
    ).count()
    total_goals_number = Goal.objects.filter(user=user).count()

    active_goals_percent = round(
        active_goals_number / total_goals_number * 100, 1
    )
    completed_goals_percent = round(
        completed_goals_number / total_goals_number * 100, 1
    )
    abandoned_goals_percent = round(
        abandoned_goals_number / total_goals_number * 100, 1
    )

    habits_number = Habit.objects.filter(user=user).count()
    habits_objects = Habit.objects.filter(user=user)

    context = {
        "active_goals_number": active_goals_number,
        "completed_goals_number": completed_goals_number,
        "abandoned_goals_number": abandoned_goals_number,
        "active_goals_percent": active_goals_percent,
        "completed_goals_percent": completed_goals_percent,
        "abandoned_goals_percent": abandoned_goals_percent,
        "habits_number": habits_number,
        "habits_objects": habits_objects,
        "total_goals_number": total_goals_number
    }

    return render(request, "index.html", context=context)


class GoalListView(LoginRequiredMixin, generic.ListView):
    model = Goal
    template_name = "goal/goal_list.html"
    context_object_name = "goal_list"
    paginate_by = 5
    queryset = Goal.objects.all()
    ordering = ["created_at"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GoalListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name")

        context["search_form"] = GoalNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        user = self.request.user
        name = self.request.GET.get("name")
        queryset = super().get_queryset()

        if name:
            return self.queryset.filter(
                name__icontains=name,
                user=user
            )

        return queryset.filter(user=user)


class GoalActiveListView(LoginRequiredMixin, generic.ListView):
    model = Goal
    template_name = "goal/goal_list_active.html"
    context_object_name = "goal_list_active"
    paginate_by = 5
    queryset = Goal.objects.filter(status="active")

    def get_queryset(self):
        user = self.request.user
        return Goal.objects.filter(user=user, status="active")


class GoalCompletedListView(LoginRequiredMixin, generic.ListView):
    model = Goal
    template_name = "goal/goal_list_completed.html"
    context_object_name = "goal_list_completed"
    paginate_by = 5
    queryset = Goal.objects.filter(status="completed")

    def get_queryset(self):
        user = self.request.user
        return Goal.objects.filter(user=user, status="completed")


class GoalAbandonedListView(LoginRequiredMixin, generic.ListView):
    model = Goal
    template_name = "goal/goal_list_abandoned.html"
    context_object_name = "goal_list_abandoned"
    paginate_by = 5
    queryset = Goal.objects.filter(status="abandoned")

    def get_queryset(self):
        user = self.request.user
        return Goal.objects.filter(user=user, status="abandoned")


class GoalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Goal
    template_name = "goal/goal_confirm_delete.html"
    success_url = reverse_lazy("tracker:goal-list")


class GoalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Goal
    fields = "__all__"
    template_name = "goal/goal_form.html"

    def get_success_url(self) -> HttpResponse:
        return reverse("tracker:goal-detail", kwargs={"pk": self.kwargs["pk"]})


@login_required
def goal_toggle_status(request, pk):
    goal = get_object_or_404(Goal, pk=pk)
    if goal.status == "active":
        goal.status = "completed"
    else:
        goal.status = "active"
    goal.save()
    return HttpResponseRedirect(reverse_lazy("tracker:goal-detail", args=[pk]))


@login_required
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


class GoalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Goal
    template_name = "goal/goal_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goal_stages"] = self.object.stages.all()
        context["goal_commentaries"] = self.object.commentaries.all()
        context["form"] = GoalCommentaryForm
        return context


class GoalStageCreateView(LoginRequiredMixin, generic.CreateView):
    model = GoalStage
    form_class = GoalCreationStageForm
    template_name = "goal/goalstage_form.html"

    def form_valid(self, form):
        form.instance.goal_id = self.kwargs["goal_id"]
        return super().form_valid(form)

    def get_success_url(self) -> HttpResponse:
        return reverse(
            "tracker:goal-detail",
            kwargs={"pk": self.kwargs["goal_id"]}
        )


class GoalStageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = GoalStage
    template_name = "goal/goalstage_confirm_delete.html"
    success_url = reverse_lazy("tracker:goal-list")

    def get_success_url(self) -> HttpResponse:
        return reverse(
            "tracker:goal-detail",
            kwargs={"pk": self.kwargs["goal_id"]}
        )


class GoalStageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = GoalStage
    fields = "__all__"
    template_name = "goal/goalstage_form.html"
    success_url = reverse_lazy("tracker:goal-list")

    def get_success_url(self) -> HttpResponse:
        return reverse(
            "tracker:goal-detail",
            kwargs={"pk": self.kwargs["goal_id"]}
        )


@login_required
def goal_stage_toggle_status(request, goal_id, pk) -> HttpResponseRedirect:
    goal_stage = get_object_or_404(GoalStage, pk=pk)
    if goal_stage.status == "active":
        goal_stage.status = "completed"
    else:
        goal_stage.status = "active"
    goal_stage.save()
    return HttpResponseRedirect(
        reverse_lazy(
            "tracker:goal-detail",
            args=[goal_id]
        )
    )


@login_required
def goal_stage_toggle_status_abandoned(
        request,
        goal_id,
        pk
) -> HttpResponseRedirect:

    goal_stage = get_object_or_404(GoalStage, pk=pk)
    if goal_stage.status == "abandoned":
        goal_stage.status = "active"
    else:
        goal_stage.status = "abandoned"
    goal_stage.save()

    return HttpResponseRedirect(
        reverse_lazy(
            "tracker:goal-detail",
            args=[goal_id]
        )
    )


class HabitListView(LoginRequiredMixin, generic.ListView):
    model = Habit
    template_name = "habit/habit_list.html"
    paginate_by = 5
    queryset = Habit.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HabitListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name")

        context["search_form"] = HabitNameSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        user = self.request.user
        name = self.request.GET.get("name")
        queryset = super().get_queryset()

        if name:
            return self.queryset.filter(
                name__icontains=name,
                user=user
            )

        return queryset.filter(user=user)


class HabitCreateView(LoginRequiredMixin, generic.CreateView):
    model = Habit
    template_name = "habit/habit_form.html"
    success_url = reverse_lazy("tracker:habit-list")
    form_class = HabitCreationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HabitDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Habit
    template_name = "habit/habit_confirm_delete.html"
    success_url = reverse_lazy("tracker:habit-list")


class HabitUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Habit
    fields = "__all__"
    template_name = "habit/habit_form.html"

    def get_success_url(self) -> HttpResponse:
        return reverse(
            "tracker:habit-detail",
            kwargs={"pk": self.kwargs["pk"]}
        )


class HabitDetailView(LoginRequiredMixin, generic.DetailView):
    model = Habit
    template_name = "habit/habit_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commentary_form"] = HabitCommentaryForm()
        context["habit_commentaries"] = self.object.commentaries.all()
        context["day_completion_form"] = HabitDayCompletionForm()
        total_days = (date.today() - self.object.created_at.date()).days
        context["total_days"] = total_days + 1
        context["completed_days"] = self.object.habit_completions.filter(
            status="completed"
        ).count()

        status = self.object.habit_completions
        context["completion_status_today"] = status.filter(
            complete_date=date.today()
        ).first()

        context["not_completed_days"] = self.object.habit_completions.filter(
            status="not_completed"
        ).count()

        context["ignored_days"] = (
            context["total_days"]
            - (context["completed_days"]
               + context["not_completed_days"])
        )

        context["update_completion_form"] = HabitDayCompletionForm(
            instance=context["completion_status_today"]
        ) if context["completion_status_today"] else None

        context["progress_percent"] = round(
            100 * (context["completed_days"] / context["total_days"]), 2
        ) if context["total_days"] else 0

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
                f"Habit '{habit.name}' marked as "
                f"'{completion.get_status_display()}' for today."
            )
        return redirect("tracker:habit-detail", pk=habit.pk)


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
        return HttpResponseRedirect(
            reverse_lazy(
                "tracker:goal-detail",
                kwargs={"pk": self.kwargs["pk"]}
            )
        )

    def get_success_url(self) -> HttpResponse:
        return reverse_lazy(
            "tracker:goal-detail",
            kwargs={"pk": self.kwargs["pk"]}
        )


class CommentaryHabitCreateView(LoginRequiredMixin, generic.CreateView):
    model = Commentary
    form_class = HabitCommentaryForm
    template_name = "habit/habit_commentary_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["habit_id"] = self.kwargs["pk"]
        return context

    def form_valid(self, form) -> HttpResponseRedirect:
        habit = Habit.objects.get(pk=self.kwargs["pk"])
        commentary = form.save(commit=False)
        commentary.user = self.request.user
        commentary.save()
        commentary.habits.add(habit)
        commentary.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "tracker:habit-detail",
                kwargs={"pk": self.kwargs["pk"]}
            )
        )

    def get_success_url(self) -> HttpResponse:
        return reverse_lazy(
            "tracker:habit-detail",
            kwargs={"pk": self.kwargs["pk"]}
        )
