from django.db import models
from django.contrib.auth.models import User

class SavedLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_locations')
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'latitude', 'longitude')

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude}) by {self.user.username}"
