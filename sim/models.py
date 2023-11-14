from django.db import models
from django.contrib.auth import get_user_model

class Photos(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    post_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)