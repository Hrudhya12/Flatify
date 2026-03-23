from django.db import models
from django.contrib.auth.models import User


class Flat(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)  # rotation position

    def __str__(self):
        return self.user.username


class TaskHistory(models.Model):
    TASK_TYPE_CHOICES = [
        ('cleaning', 'Cleaning'),
        ('essentials', 'Essentials'),
    ]

    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task_type}"