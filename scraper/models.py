from django.db import models

class TempRecipe(models.Model):
    title = models.CharField(max_length = 100, null=False, blank=False)
    link = models.CharField(max_length = 100, null=False, blank=False)
    desc = models.CharField(max_length = 200)
    snippet = models.CharField(max_length = 100)
    img = models.CharField(max_length = 100, default='')
    selected = models.BooleanField(default=False)

class FullRecipe(models.Model):
    title = models.CharField(max_length = 100, null=False, blank=False)
    link = models.CharField(max_length = 100, null=False, blank=False)
    desc = models.CharField(max_length = 200)
    steps = models.CharField(max_length=500)
    meta = models.CharField(max_length=300)
    nutrition = models.CharField(max_length=300)
    
class Ingredient(models.Model):
    recipe = models.ForeignKey(FullRecipe, on_delete=models.CASCADE)
    ingredient = models.CharField(max_length = 100, null=False, blank=False) 

