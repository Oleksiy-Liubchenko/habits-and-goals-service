from django.urls import path, include
from tracker.views import (
    GoalListView,
    GoalCreateView,
    GoalDetailView,
    GoalStageCreateView,
    HabitListView,
    HabitCreateView,
    HabitDetailView,
    NoteCreateView,
    CommentaryCreateView
)


urlpatterns = [
    path(
        "goals/",
        GoalListView.as_view(),
        name="goal-list"
    ),
    path(
        "goals/create/",
        GoalCreateView.as_view(),
        name="goal-create"
    ),
    path(
        "goals/<int:pk>/",
        GoalDetailView.as_view(),
        name="goal-detail"
    ),
    # add update view. do not forget
    path(
        "goals/create/stage/",
        GoalStageCreateView.as_view(),
        name="goal-create-stage"
    ),
    path(
        "habits/",
        HabitListView.as_view(),
        name="habit-list"
    ),
    path(
        "habits/create/",
        HabitCreateView.as_view(),
        name="habit-create"
    ),
    path(
        "habits/<int:pk>/",
        HabitDetailView.as_view(),
        name="habit-detail"
    ),
    # add update view. do not forget
    path(
        "habits/<int:pk>/create/note/",
        NoteCreateView.as_view(),
        name="habit-note-create"
    ),
    path(
        "goals/<int:pk>/create/note/",
        NoteCreateView.as_view(),
        name="goal-note-create"
    ),
    path(
        "habits/<int:pk>/create/commentary/",
        CommentaryCreateView.as_view(),
        name="habit-commentary-create"
    ),
    path(
        "goals/<int:pk>/create/commentary/",
        CommentaryCreateView.as_view(),
        name="goal-commentary-create"
    ),
]

app_name = "tracker"
