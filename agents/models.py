from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.conf import settings

class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=(('admin', 'Admin'), ('analyst', 'Analyst')))
    sex = models.CharField(max_length=20)
    oboruduvania = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

# ... rest of your models ...

def post_user_yaratish_signal(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_yaratish_signal, sender=settings.AUTH_USER_MODEL)
