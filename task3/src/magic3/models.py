from django.db import models
from django.contrib.postgres.fields import JSONField


class Elixir(models.Model):
    name = models.CharField(max_length=128)
    ingredients = JSONField()
    difficulty_level = models.CharField(max_length=10)

    def __str__(self):
        return '{} ({})'.format(self.name, self.difficulty_level)