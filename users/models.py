from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200, default='test name')
    # lastname = models.CharField(default='testname', max_length=180)
    # firstname = models.CharField(default='testgivenname', max_length=180)

    def __str__(self):
        return f'{self.user.username} Account'

