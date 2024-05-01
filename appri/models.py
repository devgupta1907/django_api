from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=20)
    roll = models.IntegerField()
    city = models.CharField(max_length=20)


class Todo(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
# Create your models here.
