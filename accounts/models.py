from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    telegram_verification_code = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def generate_verification_code(self):
        if not self.telegram_verification_code:
            self.telegram_verification_code = str(uuid.uuid4())[:8]
            self.save()
        return self.telegram_verification_code

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()
