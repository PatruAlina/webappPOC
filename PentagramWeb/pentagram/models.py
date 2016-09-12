from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Photo(models.Model):
    user=models.ForeignKey(User)
    photo=models.ImageField(default="NULL")
    like=models.IntegerField(default=0)


class Comment(models.Model):
    user=models.ForeignKey(User)
    comment=models.TextField()
    photo=models.ForeignKey(Photo)