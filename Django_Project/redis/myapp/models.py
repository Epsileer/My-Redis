from django.db import models

# Create your models here.
class Data(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    ttl = models.IntegerField()

class Zdata(models.Model):
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
	score = models.IntegerField()