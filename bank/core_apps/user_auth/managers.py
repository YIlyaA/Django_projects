import random 
import string
from os import getenv
from typing import Optional, Any

from click import Option
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

def generate_username() -> str:
    bank_name = getenv('BANK_NAME')
    words = bank_name.split()
    prefix = "".join([word[0] for word in words]).upper()
    remaining_length = 12 - len(prefix) - 1
    random_chars = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=remaining_length)
    )
    username = f"{prefix}-{random_chars}"
    return username


def validate_email_address(email: str) -> None:
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_("Enter a valid email address"))


class UserManager(DjangoUserManager):
    # private method 
    def _create_user(self, email:str, password:str, **extra_fields: Any):
        if not email:
            raise ValueError(_("An email address must be provided."))
        if not password:
            raise ValueError(_("A password address must be provided."))

        username = generate_username()
        email = self.normalize_email(email)
        validate_email_address(email)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.password = make_password(password)  # hash password
        user.save(using=self._db)
        return user

    # public ,ethod
    def create_user(self, email:str, password: Optional[str]=None, **extra_fields: Any):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: Optional[str]=None, **extra_fields: Any):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self._create_user(email, password, **extra_fields)
