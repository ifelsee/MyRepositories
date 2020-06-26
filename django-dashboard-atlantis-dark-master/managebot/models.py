from django.db import models

# Create your models here.

class Custom_Command(models.Model):
    guild_id = models.CharField(max_length=(18),blank=False)
    guild_name = models.CharField(max_length=(100),blank=False)
    command = models.CharField(max_length=(100),blank=False)
    response = models.TextField(max_length=(200),blank=False)

    # NOTE: options
    dm_response = models.CharField(max_length=(200),blank=False)
    allowed_roles = models.CharField(max_length=(200),blank=False)
    ignored_roles = models.CharField(max_length=(200),blank=False)
    response_channel = models.CharField(max_length=(200),blank=False)
    def __str__(self):
        return self.guild_name
