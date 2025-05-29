from django.core.management.base import BaseCommand
from services.models import Service, ServiceProvider

class Command(BaseCommand):
    help = 'Populate database with demo data'

    def handle(self, *args, **options):
        # Create services
        services_data = [
            {'name': 'House Cleaning', 'category': 'Cleaning', 'description': 'Professional house cleaning service'},
            {'name': 'Office Cleaning', 'category': 'Cleaning', 'description': 'Commercial office cleaning'},
            {'name': 'Plumbing Repairs', 'category': 'Plumbing', 'description': 'General plumbing repairs and maintenance'},
            {'name': 'Math Tutoring', 'category': 'Tutoring', 'description': 'Mathematics tutoring for all grades'},
            {'name': 'Car Repairs', 'category': 'Car Mechanic', 'description': 'General car repairs and maintenance'},
            {'name': 'Car Wash & Detail', 'category': 'Car Detailing', 'description': 'Professional car cleaning and detailing'},
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f"Created service: {service.name}")
        
        # Create service providers
        providers_data = [
            # Cleaning
            {'name': 'Thuli Mthembu', 'phone': '+27123456789', 'location': 'Sandton CBD', 'rate': 180, 'services': ['House Cleaning']},
            {'name': 'Sarah Johnson', 'phone': '+27123456790', 'location': 'Rosebank', 'rate': 200, 'services': ['House Cleaning', 'Office Cleaning']},
            {'name': 'Grace Ndaba', 'phone': '+27123456791', 'location': 'Morningside', 'rate': 160, 'services': ['House Cleaning']},
            {'name': 'Linda Mabaso', 'phone': '+27123456792', 'location': 'Bryanston', 'rate': 190, 'services': ['House Cleaning']},
            {'name': 'Mary Khumalo', 'phone': '+27123456793', 'location': 'Wendywood', 'rate': 170, 'services': ['House Cleaning']},
            
            # Plumbing
            {'name': 'Johan van Wyk', 'phone': '+27123456794', 'location': 'Sandton', 'rate': 350, 'services': ['Plumbing Repairs']},
            {'name': 'Mike Botha', 'phone': '+27123456795', 'location': 'Sandton CBD', 'rate': 320, 'services': ['Plumbing Repairs']},
            {'name': 'David Nel', 'phone': '+27123456796', 'location': 'Rosebank', 'rate': 380, 'services': ['Plumbing Repairs']},
            {'name': 'Chris Venter', 'phone': '+27123456797', 'location': 'Bryanston', 'rate': 340, 'services': ['Plumbing Repairs']},
            
            # Tutoring
            {'name': 'Dr. Priya Patel', 'phone': '+27123456798', 'location': 'Sandton', 'rate': 250, 'services': ['Math Tutoring']},
            {'name': 'James Thompson', 'phone': '+27123456799', 'location': 'Rosebank', 'rate': 200, 'services': ['Math Tutoring']},
            {'name': 'Lisa Chen', 'phone': '+27123456800', 'location': 'Morningside', 'rate': 230, 'services': ['Math Tutoring']},
            {'name': 'Robert Mthembu', 'phone': '+27123456801', 'location': 'Bryanston', 'rate': 180, 'services': ['Math Tutoring']},
            
            # Car Mechanics
            {'name': "Tony's Auto", 'phone': '+27123456802', 'location': 'Sandton', 'rate': 400, 'services': ['Car Repairs']},
            {'name': 'Quick Fix Motors', 'phone': '+27123456803', 'location': 'Rosebank', 'rate': 380, 'services': ['Car Repairs']},
            {'name': 'Sandton Car Care', 'phone': '+27123456804', 'location': 'Sandton CBD', 'rate': 420, 'services': ['Car Repairs']},
            {'name': 'Express Auto', 'phone': '+27123456805', 'location': 'Bryanston', 'rate': 360, 'services': ['Car Repairs']},
            
            # Car Detailing
            {'name': 'Shine Masters', 'phone': '+27123456806', 'location': 'Sandton', 'rate': 300, 'services': ['Car Wash & Detail']},
            {'name': 'Clean Car Co', 'phone': '+27123456807', 'location': 'Rosebank', 'rate': 280, 'services': ['Car Wash & Detail']},
            {'name': 'Detail Pro', 'phone': '+27123456808', 'location': 'Morningside', 'rate': 320, 'services': ['Car Wash & Detail']},
        ]
        
        for provider_data in providers_data:
            provider, created = ServiceProvider.objects.get_or_create(
                phone=provider_data['phone'],
                defaults={
                    'name': provider_data['name'],
                    'location': provider_data['location'],
                    'hourly_rate': provider_data['rate'],
                }
            )
            
            if created:
                # Add services to provider
                for service_name in provider_data['services']:
                    service = Service.objects.get(name=service_name)
                    provider.services.add(service)
                
                self.stdout.write(f"Created provider: {provider.name}")
        
        self.stdout.write(self.style.SUCCESS('Successfully populated demo data!'))