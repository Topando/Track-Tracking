import random

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from userprofile.models import ConfirmEmailUser

User = get_user_model()


def send_confirmation_email(user, code):
    subject = 'Подтверждение почты'
    html_content = render_to_string('authentication/email_confirmation_message.html',
                                    {'confirmation_code': code})
    text_content = strip_tags(html_content)
    try:
        user.email_user(subject, text_content)
        return True
    except Exception:
        return False


def create_token_check_email(user):
    code = random.randint(10_000, 99_999)
    ConfirmEmailUser.objects.create(
        user=user,
        code=code,
    )
    return code


def encode_user(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return token, uid


def get_user_by_token_email(token, uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return user
    return None
