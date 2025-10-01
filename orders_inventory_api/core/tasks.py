from celery import shared_task
import time


@shared_task
def hello_celery(name="Gon"):
    """
    Tarea de prueba para verificar que Celery está funcionando.
    """
    time.sleep(2)
    return f"Hola {name}, Celery está funcionando!"
