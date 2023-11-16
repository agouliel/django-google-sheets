from django.db import models
from django.contrib.auth import get_user_model
import os
from django.conf import settings

class Photos(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(blank=True, null=True) # varchar(100) in sqlite
    post_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # https://stackoverflow.com/questions/17663809/deleting-uploaded-files-in-django
    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete()
        super().delete(*args, **kwargs)