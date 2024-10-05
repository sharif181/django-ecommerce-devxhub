from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(subject, message, recipient_email):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Ensure DEFAULT_FROM_EMAIL is set in settings
        [recipient_email],
        fail_silently=False,
    )
