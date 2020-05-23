from django.db import models

# Create your models here.
class DataPoint(models.Model):
    date = models.DateField()
    begin = models.FloatField(default=0.0)
    end = models.FloatField(default=0.0)
    high = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    ratio = models.FloatField(default=0.0)


class Prediction(models.Model):
    date = models.DateField()
    predicted = models.FloatField(default=0.0)
    previous = models.FloatField(default=0.0)
    actual = models.FloatField(default=0.0, null=True)
    is_higher = models.BooleanField(default=False)
    result_ok = models.BooleanField(default=False, null=True)
