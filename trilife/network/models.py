from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    stripe_id = models.CharField(max_length=255, blank=True)
    subscribed = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        return self.name

