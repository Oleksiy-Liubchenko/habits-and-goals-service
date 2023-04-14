from django.contrib import admin
from tracker.models import Habit, Goal, User, GoalStage
from django.contrib.auth.admin import UserAdmin
# SuperUser login - test_user
# SuperUser pass - 12345678


class GoalStageInline(admin.TabularInline):
    model = GoalStage
    extra = 0


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = [
        "name", "description", "deadline",
        "created_at", "status", "user"
    ]
    list_filter = ["deadline", "user"]
    search_fields = ["name"]
    inlines = [GoalStageInline]


@admin.register(User)
class User(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("first_name", "last_name")}),
    )


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "month_goal", "created_at", "user"]
    list_filter = ["user", "created_at"]
