from django.contrib import admin
from tracker.models import Habit, Goal

# SuperUser login - test_user
# SuperUser pass - 12345678


admin.site.register(Habit)
admin.site.register(Goal)
