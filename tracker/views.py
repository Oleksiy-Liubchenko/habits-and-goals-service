from django.shortcuts import render
from django.views import generic


def index(request, pk):
    pass


class GoalListView(generic.ListView):
    pass


class GoalCreateView(generic.CreateView):
    pass


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
