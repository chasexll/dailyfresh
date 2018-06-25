from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=40)
    addressee = models.CharField(max_length=20, default='')
    uaddress = models.CharField(max_length=100, default='')
    postcode = models.CharField(max_length=6, default='')
    uphone = models.CharField(max_length=11, default='')
