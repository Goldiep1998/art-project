from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    image = models.ImageField(upload_to='images/profile-images', default='images/default.jpg')

@receiver(post_save, sender=User) 
def create_profile(sender, created, instance, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        subject = 'Welcome to ArtSellNShop!'
        message = f'Hi {instance.username}, Thank you for registering in ArtSellNShop.'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [instance.email,]
        send_mail( subject, message, email_from, recipient_list) 

def __str__(self):
    return self.user