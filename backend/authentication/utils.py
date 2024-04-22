from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()

def send_confirmation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirm_url = reverse('email_confirmation', args=[uid, token])
    confirmation_link = request.build_absolute_uri(confirm_url)

    subject = 'Подтверждение почты'
    html_content = render_to_string('authentication/email_confirmation_message.html',
                                    {'confirmation_link': confirmation_link})
    text_content = strip_tags(html_content)
    user.email_user(subject, text_content)


def get_user_by_token_email(uidb64, token):
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