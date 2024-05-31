from django.db import models

# Create your models here.
class sigup(models.Model):
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=20)
    em=models.CharField(primary_key=True,max_length=50)
    pasw=models.CharField(max_length=15)
    
class comments(models.Model):
    signup =models.CharField(max_length=50)
    comm=models.CharField(max_length=100)
    post=models.CharField(max_length=100)

    

