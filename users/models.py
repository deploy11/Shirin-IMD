from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    sinf = models.BooleanField(blank=True,null=True,default=False)
    sinf_nomi = models.CharField(max_length=500,null=True,blank=True)
    der = models.BooleanField(blank=True,null=True,default=False)
    maf = models.BooleanField(blank=True,null=True,default=False)