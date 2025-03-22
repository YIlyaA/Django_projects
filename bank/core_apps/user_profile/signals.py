from typing import Type, Any

from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from loguru import logger

from config.settings.base import AUTH_USER_MODEL
from core_apps.user_profile.models import Profile


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Type[Model], instance: Model, created: bool, **kwargs: Any
) -> None:
    if created:
        Profile.objects.create(user=instance)
        logger.info(
            f"Profile created for user {instance.first_name} {instance.last_name}"
        )


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_prodile(sender: Type[Model], instance: Model, **kwargs: Any) -> None:
    instance.profile.save()
    logger.info(f"Profile saved for user {instance.first_name} {instance.last_name}")
