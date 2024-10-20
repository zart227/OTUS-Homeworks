from django.core.mail import send_mail
from django.conf import settings


def send_contact_email(email, name, message):
    send_mail(
        subject=f"New message from {name}",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )

    send_mail(
        subject="We received your message",
        message="Thank you for contacting us. We will get back to you shortly.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
