from django.db import models
from users.models import User

# Create your models here.
class Group(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(null=True)
    users=models.ManyToManyField(User)

    def __str__(self):
        return self.name