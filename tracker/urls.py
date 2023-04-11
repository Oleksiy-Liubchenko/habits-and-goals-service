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
    CommentaryGoalCreateView,
    CommentaryHabitCreateView,
    index,
    GoalDeleteView,
    GoalUpdateView,
    GoalStageUpdateView,
    GoalStageDeleteView,
    # HabitDayCompletionUpdateView
)


urlpatterns = [
    path(
        "",
        index,
        name="index"
    ),
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
    path(
        "goals/<int:pk>/delete",
        GoalDeleteView.as_view(),
        name="goal-delete"
    ),
    path(
        "goals/<int:pk>/update",
        GoalUpdateView.as_view(),
        name="goal-update"
    ),
    # add update view. do not forget
    path(
        "goals/<int:goal_id>/create/stage/",
        GoalStageCreateView.as_view(),
        name="goal-create-stage"
    ),
    path(
        "goals/<int:goal_id>/update/stage/<int:pk>/",
        GoalStageUpdateView.as_view(),
        name="goal-update-stage" # спросить у чата, что не так, как передавть еще пк айди ...
    ),
    # path(
    #     "goals/<int:goal_id>/update/stage/",
    #     GoalStageUpdateView.as_view(),
    #     name="goal-update-stage"
    # ),
    path(
        "goals/<int:goal_id>/delete/stage/<int:pk>/",
        GoalStageDeleteView.as_view(),
        name="goal-delete-stage"
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
    # path(
    #     "habits/<int:pk>/completion/<int:completion_pk>/update/",
    #     HabitDayCompletionUpdateView.as_view(),
    #     name="habit-completion-update"
    # ),

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
        CommentaryHabitCreateView.as_view(),
        name="habit-commentary-create"
    ),
    path(
        "goals/<int:pk>/create/commentary/",
        CommentaryGoalCreateView.as_view(),
        name="goal-commentary-create"
    ),
]

app_name = "tracker"
