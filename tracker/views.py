from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from tracker.forms import (
    GoalCreationForm,
    GoalCreationStageForm,
    GoalCommentaryForm,
    HabitCreationForm,
    HabitCommentaryForm,
    GoalNameSearchForm,
    HabitNameSearchForm, HabitLogForm,
)
from tracker.models import (
    Goal,
    GoalStage,
    Habit,
    Commentary
)


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        queryset = Goal.objects.filter(user=user)
        statuses = ["active", "completed", "abandoned"]
        goals_number = {
            f"{status}_goals_number": queryset.filter(status=status).count()
            for status in statuses
        }
        total_goals_number = queryset.count()

        if total_goals_number == 0:
            total_goals_number = float("inf")

        goals_percent = {
            f"{field_name.split('_number')[0]}_percent":
                round(goal_number / total_goals_number * 100, 1)
            for field_name, goal_number in goals_number.items()
        }

        habits_objects = Habit.objects.filter(user=user)
        habits_number = habits_objects.count()

        context = {
            **goals_number,
            **goals_percent,
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
            queryset = queryset.filter(name__icontains=name)

        status = self.request.GET.get("status")

        queryset = queryset.filter(user=user)

        if status in ["completed", "abandoned", "active"]:
            queryset = queryset.filter(status=status)
        return queryset


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


class GoalToggleStatusView(View):
    def get(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        goal.status = "completed" if goal.status == "active" else "active"
        goal.save()
        return HttpResponseRedirect(
            reverse_lazy("tracker:goal-detail", args=[pk])
        )


class GoalToggleAbandonedStatusView(View):
    def get(self, request, pk):
        goal = get_object_or_404(Goal, pk=pk)
        goal.status = "active" if goal.status == "abandoned" else "abandoned"
        goal.save()
        return HttpResponseRedirect(
            reverse_lazy("tracker:goal-detail", args=[pk])
        )


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


class GoalToggleStageStatusView(View):
    def get(self, request, goal_id, pk):
        goal_stage = get_object_or_404(GoalStage, pk=pk)
        complete = "completed"
        active = "active"
        goal_stage.status = complete if goal_stage.status == active else active
        goal_stage.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "tracker:goal-detail",
                args=[goal_id]
            )
        )


class GoalToggleStageAbandonedStatusView(View):
    def get(self, request, goal_id, pk):
        goal_stage = get_object_or_404(GoalStage, pk=pk)
        abandon = "abandoned"
        active = "active"
        goal_stage.status = active if goal_stage.status == abandon else abandon
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
        total_days = (date.today() - self.object.created_at.date()).days
        context["total_days"] = total_days + 1

        context["completed_days_log"] = self.object.logs.filter(
            completed="True"
        ).count()
        context["not_completed_days_log"] = self.object.logs.filter(
            completed="False"
        ).count()

        context["ignored_days"] = (
            context["total_days"]
            - (context["completed_days_log"]
               + context["not_completed_days_log"])
        )

        context["progress_percent"] = round(
            100 * (context["completed_days_log"] / context["total_days"]), 2
        ) if context["total_days"] else 0

        context["today_date"] = f"{date.today()}"
        context["habit_log_form"] = HabitLogForm()

        dates = self.object.logs.all().dates("created_at", "day")
        context["filled_dates"] = [d.strftime("%Y-%m-%d") for d in dates]

        return context

    def post(self, request, *args, **kwargs):
        habit = self.get_object()
        form = HabitLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.habit = habit
            log.save()

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
