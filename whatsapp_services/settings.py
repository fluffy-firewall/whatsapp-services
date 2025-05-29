# Production settings
import os
if 'RAILWAY_ENVIRONMENT' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    
    # Fix CSRF for admin
    CSRF_TRUSTED_ORIGINS = [
        'https://whatsapp-services-production-1e47.up.railway.app'
    ]
    
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
