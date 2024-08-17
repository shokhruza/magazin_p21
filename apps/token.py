from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

from celery import shared_task
from django.core.mail import EmailMessage


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


account_activation_token = TokenGenerator()



@shared_task
def send_to_email_task(subject, message, _email):
    email = EmailMessage(subject, message, to=[_email])
    email.content_subtype = 'html'
    email.send()
    return {'status': 'yuborildi', "email": _email}