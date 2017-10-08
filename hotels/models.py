from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class FBUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    #proile_pic = models.URLField(max_length=1024, blank=True)
    timezone = models.DecimalField(max_digits=4,decimal_places=2, blank=True)
    gender = models.CharField(max_length=15, blank=True)
    is_payment_enabled = models.BooleanField(blank=True)
    fb_userId = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def save_to_db(self):
        self.timestamp = timezone.now()
        self.save()

    def __str__(self):
        return self.first_name

class Postbacks(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=15, blank=True)
    postback = models.CharField(max_length=50)
    fb_userId = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def save_to_db(self):
        self.timestamp = timezone.now()
        self.save()
