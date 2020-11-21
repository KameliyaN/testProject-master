from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default='SOME STRING')
    username = models.CharField(max_length=150,blank=True,default='SOME STRING')
    first_name = models.CharField(max_length=200, blank=True,default='SOME STRING')
    last_name = models.CharField(max_length=200, blank=True,default='SOME STRING')
    email = models.CharField(max_length=200, blank=True, default='SOME STRING')
    picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'
