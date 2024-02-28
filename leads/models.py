from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Lead(models.Model):
    STATUS_CHOICES = (
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('master', 'Master'),
        ('slave', 'Slave'),
    )
    ismi = models.CharField(max_length=20)
    familiyasi = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)  # Ensure IDs are unique
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name='leads', null=True, blank=True, on_delete=models.SET_NULL)
    data = models.DateTimeField()
    vremya = models.DateTimeField()
    status_obnardjil = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sex = models.CharField(max_length=20)
    oboruduvania = models.CharField(max_length=20)  # Corrected field name to match form
    uchastok = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.familiyasi

def post_user_yaratish_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_yaratish_signal, sender=User)
