from django.apps import AppConfig


class CeleryTaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_task'

    def ready(self):
        import celery_task.views