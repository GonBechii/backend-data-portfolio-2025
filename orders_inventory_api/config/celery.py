import os
from celery import Celery

# Configuracion de settings de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'orders_inventory_api.config.settings')

# Nombre del proyecto (recomiendo que sea único)
app = Celery('orders_inventory_api')

# Prefijo Celery_ en settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodescubre tasks.py en cada app instalada
app.autodiscover_tasks()
