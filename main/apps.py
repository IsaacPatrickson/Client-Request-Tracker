from django.apps import AppConfig
import os
import logging

logger = logging.getLogger(__name__)

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    def ready(self):
        from .utils.permissions import create_limited_users_permission_group
        from .utils.seed_example_data import seed_example_clients
        try:
            create_limited_users_permission_group()
            seed_example_clients()
        except Exception:
            pass
        
        if os.environ.get('RUN_MAIN') == 'true' and os.environ.get('DJANGO_ENV') != 'production':
            try:
                from .utils.seed_users import seed_example_users
                created = seed_example_users()
                if created:
                    logger.info(f"Seeded users: {', '.join(created)}")
            except Exception as e:
                logger.error(f"Failed to seed users: {e}")
        
        
