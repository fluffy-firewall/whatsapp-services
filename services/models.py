from django.db import models
from django.utils import timezone
import json

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    services = models.ManyToManyField(Service)
    location = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.JSONField(default=dict)  # {"monday": ["09:00-17:00"], ...}
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"
    
    def get_services_list(self):
        return ", ".join([service.name for service in self.services.all()])

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('provider_notified', 'Provider Notified'),
        ('confirmed', 'Confirmed'),
        ('payment_sent', 'Payment Link Sent'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    client_phone = models.CharField(max_length=15)
    client_name = models.CharField(max_length=100, blank=True)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    requested_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    service_direction = models.CharField(max_length=20, choices=[
        ('provider_to_client', 'Provider comes to client'),
        ('client_to_provider', 'Client goes to provider')
    ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_url = models.URLField(null=True, blank=True)
    payment_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.client_phone} - {self.service.name}"