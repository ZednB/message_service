from celery import Celery

celery_app = Celery(
    'message_service',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.task_routes = {"tasks.send_telegram_message": {"queue": "telegram"}}
celery_app.autodiscover_tasks(['telegram_bot'])
