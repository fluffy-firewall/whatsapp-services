from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from django.conf import settings
import json
import re
from datetime import datetime, timedelta
from .models import Service, ServiceProvider, Booking
from .whatsapp_bot import WhatsAppBot

def home(request):
    return HttpResponse("WhatsApp Services Marketplace is running!")

@csrf_exempt
@require_POST
def whatsapp_webhook(request):
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Get message data from Twilio
        from_number = request.POST.get('From', '')
        message_body = request.POST.get('Body', '').strip()
        
        # Initialize the bot
        bot = WhatsAppBot()
        
        # Process the message
        response_message = bot.process_message(from_number, message_body)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_message)
        
        return HttpResponse(str(resp))
        
    except Exception as e:
        print(f"Error in WhatsApp webhook: {str(e)}")
        resp = MessagingResponse()
        resp.message("Sorry, I'm having technical difficulties. Please try again later.")
        return HttpResponse(str(resp))