from django.db import models

# Create your models here.

class Custom_Command(models.Model):
    guild_id = models.CharField(max_length=(18),blank=False)
    command = models.CharField(max_length=(100),blank=False)
    response = models.CharField(max_length=(100),blank=False)
