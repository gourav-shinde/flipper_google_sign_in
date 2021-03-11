from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

User._meta.get_field('email')._unique = True

class UserType(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    selected=models.BooleanField(default=False)
    HR=models.BooleanField(default=False)

# Create your models here.
@receiver(post_save,sender=User)
def create_usertype(sender,instance=None,created=False,**kwargs):
    if created:
        UserType.objects.create(user=instance)