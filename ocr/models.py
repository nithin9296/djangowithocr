from django.db import models
import os
from django import forms
from django.conf import settings
from django.urls import reverse

# Create your models here.


    
class trialbalance2017(models.Model):
    description = models.CharField(max_length=100)
    debit = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    slug = models.CharField(max_length=100,
                            default='description')
