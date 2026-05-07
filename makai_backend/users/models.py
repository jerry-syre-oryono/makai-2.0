from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    department = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    staff_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username # Changed from self.email as email might not be unique/required by default in AbstractUser unless specified, keeping it safe with username.
