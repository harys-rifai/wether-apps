from django.db import models
from django.contrib.auth.models import User
from weather.models import SavedLocation

class WeatherAlertRule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_rules')
    location = models.ForeignKey(SavedLocation, on_delete=models.CASCADE, related_name='alert_rules')
    
    alert_on_temp_high = models.BooleanField(default=True)
    temp_high_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=35.0)
    
    alert_on_temp_low = models.BooleanField(default=False)
    temp_low_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    
    alert_on_wind_high = models.BooleanField(default=True)
    wind_high_threshold = models.DecimalField(max_digits=5, decimal_places=2, default=15.0)
    
    alert_on_storm = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    last_alert_sent = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Alert for {self.location.name} ({self.user.username})"
