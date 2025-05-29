from django.contrib import admin
from .models import Service, ServiceProvider, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'description']
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'location', 'hourly_rate', 'rating', 'is_active']
    list_filter = ['location', 'is_active', 'services']
    search_fields = ['name', 'phone', 'location']
    filter_horizontal = ['services']
    
    def get_services_list(self, obj):
        return obj.get_services_list()
    get_services_list.short_description = 'Services'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_phone', 'provider', 'service', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    search_fields = ['client_phone', 'provider__name', 'service__name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']