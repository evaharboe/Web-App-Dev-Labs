from django.db import models
from django.core.exceptions import ValidationError
import re

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.TextField(max_length=256)
    image = models.ImageField(upload_to='media')
    slug = models.SlugField(max_length=64, unique=True, null=False, blank=False)
    # deleting a project destroys its boards, lists, tasks, and labels*
    # a project can exist without any boards, lists, or labels

class Board(models.Model):
    # a project, which must exist*
    title = models.CharField(max_length=64, unique=True) # unique within a project not necessaraly across other projects
    # boards can exist without lists

class List(models.Model):
    # a board, which must exist*
    title = models.CharField(max_length=64, unique=True, null=False, blank=False) # unique within a board not necessaraly across other boards
    position = models.PositiveIntegerField()

class Task(models.Model):
    task_no = models.IntegerField(primary_key=True)
    # a list, which must exist*
    title = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(max_length=512)
    priority = models.CharField(max_length=1, choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], default='M') # is this an enum?
    story_points = models.PositiveIntegerField(min_value=0, max_value=100, divisable_by=5)
    labels = models.ManyToManyField('Label')

class Label(models.Model):
    title = models.CharField(max_length=32, unique=True, null=False) # unique within project only
    colour = models.CharField(max_length=7) # hex color code
    # a project, which must exist, and zero to many tasks*

    def is_valid_hex(self, colour):
        return bool(re.match(r'^#([A-Fa-f0-9]{6})$', colour))

    def clean(self):
        # Call is_valid_hex with self.colour
        if not self.is_valid_hex(self.colour):
            raise ValidationError('Invalid hex color code')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
