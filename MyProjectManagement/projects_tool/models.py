from django.db import models
from django.core.exceptions import ValidationError
import re
from django.core.validators import MinValueValidator, MaxValueValidator

# custom validator
def division_by_five(value):
    if value % 5 != 0:
        raise ValidationError(
            ('The value %(value)s must be divisible by 5.'),
            params={'value': value},
        )

class Project(models.Model):
    title = models.CharField(max_length=64, unique=True, null=False, blank=False)
    description = models.TextField(max_length=256, blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    slug = models.SlugField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return self.title

class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=True)

    class Meta:
        unique_together = ('project', 'title')

    def __str__(self):
        return self.title

class List(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=True, null=False, blank=False)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('board', 'title')
        
    def __str__(self):
        return self.title

class Task(models.Model):
    task_no = models.IntegerField(primary_key=True)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=False, blank=False)
    description = models.TextField(max_length=512, blank=True, null=True)
    priority = models.CharField(max_length=1, choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], default='M')
    story_points = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
            division_by_five
        ]
    )
    labels = models.ManyToManyField('Label')


class Label(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=False)
    colour = models.CharField(max_length=7)

    class Meta:
        unique_together = ('project', 'title')

    def is_valid_hex(self, colour):
        return bool(re.match(r'^#([A-Fa-f0-9]{6})$', colour))

    def clean(self):
        if not self.is_valid_hex(self.colour):
            raise ValidationError('Invalid hex color code')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

