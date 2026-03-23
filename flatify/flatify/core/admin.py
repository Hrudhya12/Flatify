from django.contrib import admin
from .models import Flat, Profile, TaskHistory

admin.site.register(Flat)
admin.site.register(Profile)
admin.site.register(TaskHistory)