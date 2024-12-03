from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



# Create your models here.
class IoTDevice(models.Model): 
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance')
    ]
    device_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='offline')
    last_seen = models.DateTimeField(auto_now=True)

     def update_last_seen(self):
        """Update last seen timestamp"""
        self.last_seen = timezone.now()
        self.save()

class DeviceData(models.Model):
    device = models.ForeignKey(IoTDevice, related_name='data_logs', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    additional_data = models.JSONField(null=True, blank=True)