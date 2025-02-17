from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger

def send_otp_email(email, otp):
    subject = _('Your OTP code for Login')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "otp": otp,
        "site_name": settings.SITE_NAME,
        "expiry_time": settings.OTP_EXPIRETION,
    }
    html_email = render_to_string('emails/otp_email.html', context)
    plain_email = strip_tags(html_email)   # delete all html tags
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)  # allows to send both plain text and html content
    email.attach_alternative(html_email, "text/html")   # attachs html version of email
    try:
        email.send()
        logger.info(f"OTP email sent successfully to: {email}")
    except Exception as e:
        logger.exception(f"Failed to send OTP email to {email}: Error {str(e)}")


def send_account_locked_email(self):
    subject = _('Your account has been locked')
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [self.email]
    context = {
        "user": self.user,
        "site_name": settings.SITE_NAME,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
    }
    html_email = render_to_string('emails/account_locked.html', context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    try:
        email.send()
        logger.info(f"Account locked email sent to: {self.email}")
    except Exception as e:
        logger.exception(f"Failed to send accout locked email to {self.email}: Error {str(e)}")
