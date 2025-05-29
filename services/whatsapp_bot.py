import re
from datetime import datetime, timedelta
from django.utils import timezone
from twilio.rest import Client
from django.conf import settings
from .models import Service, ServiceProvider, Booking

class WhatsAppBot:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
    def process_message(self, from_number, message_body):
        """Main message processing logic"""
        message_lower = message_body.lower().strip()
        
        # Check if this is a provider response (YES/NO)
        if message_lower in ['yes', 'no', 'y', 'n']:
            return self.handle_provider_response(from_number, message_lower)
        
        # Check if this is a booking selection (1, 2, 3)
        if message_lower in ['1', '2', '3']:
            return self.handle_booking_selection(from_number, message_lower)
        
        # Check for service request
        service_request = self.parse_service_request(message_body)
        if service_request:
            return self.handle_service_request(from_number, service_request)
        
        # Default response
        return self.get_help_message()
    
    def parse_service_request(self, message):
        """Parse user message to extract service, location, and time"""
        message_lower = message.lower()
        
        # Service keywords
        services_map = {
            'clean': 'Cleaning',
            'plumb': 'Plumbing', 
            'tutor': 'Tutoring',
            'mechanic': 'Car Mechanic',
            'car wash': 'Car Detailing',
            'detail': 'Car Detailing'
        }
        
        # Location keywords (Sandton areas)
        locations = ['sandton', 'rosebank', 'morningside', 'bryanston', 'wendywood']
        
        # Time keywords
        time_keywords = ['today', 'tomorrow', 'monday', 'tuesday', 'wednesday', 
                        'thursday', 'friday', 'saturday', 'sunday']
        
        detected_service = None
        detected_location = None
        detected_time = None
        
        # Find service
        for keyword, service in services_map.items():
            if keyword in message_lower:
                detected_service = service
                break
        
        # Find location
        for location in locations:
            if location in message_lower:
                detected_location = location.capitalize()
                break
        
        # Find time (simplified)
        for time_word in time_keywords:
            if time_word in message_lower:
                detected_time = time_word
                break
        
        if detected_service and detected_location:
            return {
                'service': detected_service,
                'location': detected_location,
                'time': detected_time or 'not specified'
            }
        
        return None
    
    def handle_service_request(self, from_number, service_request):
        """Handle a parsed service request"""
        try:
            # Find matching service
            service = Service.objects.filter(name__icontains=service_request['service']).first()
            if not service:
                return f"Sorry, I couldn't find '{service_request['service']}' service. Available services: Cleaning, Plumbing, Tutoring, Car Mechanic, Car Detailing."
            
            # Find available providers
            providers = ServiceProvider.objects.filter(
                services=service,
                location__icontains=service_request['location'],
                is_active=True
            ).order_by('-rating')[:3]
            
            if not providers:
                return f"Sorry, no {service_request['service']} providers available in {service_request['location']} right now."
            
            # Create response with provider options
            response = f"Great! I found these {service_request['service']} providers in {service_request['location']}:\n\n"
            
            for i, provider in enumerate(providers, 1):
                response += f"{i}️⃣ {provider.name}\n"
                response += f"   Rate: R{provider.hourly_rate}/hour\n"
                response += f"   Rating: ⭐{provider.rating}\n\n"
            
            response += "Reply with 1, 2, or 3 to book!"
            
            # Store the context for next message (simplified - in production use sessions/cache)
            # For now, we'll handle this in the booking selection
            
            return response
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def handle_booking_selection(self, from_number, selection):
        """Handle provider selection (1, 2, 3)"""
        # In a real implementation, you'd store user context
        # For demo, return a simplified response
        return f"Perfect! You selected option {selection}. To complete this booking, I would:\n\n1. Notify the provider\n2. Send you a payment link\n3. Share contact details after payment\n\nThis is a demo - booking flow will be completed in the next development phase!"
    
    def handle_provider_response(self, from_number, response):
        """Handle provider YES/NO responses"""
        if response.lower() in ['yes', 'y']:
            return "Great! I'll notify the client and send them the payment link."
        else:
            return "No problem. I'll find another provider for this client."
    
    def get_help_message(self):
        """Return help message"""
        return """👋 Welcome to WhatsApp Services!

I can help you book local services in Sandton. Just tell me what you need!

Example: "I need cleaning in Sandton tomorrow"

Available services:
🧹 Cleaning
🔧 Plumbing  
📚 Tutoring
🚗 Car Mechanic
✨ Car Detailing

Available areas:
📍 Sandton, Rosebank, Morningside, Bryanston, Wendywood"""