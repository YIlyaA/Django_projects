import email
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "id_no",
            "first_name",
            "middle_name",
            "last_name",
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email

    def clean_id_no(self):
        id_no = self.cleaned_data["id_no"]
        if User.objects.filter(id_no=id_no).exists():
            raise ValidationError(_("A user with that ID number already exists."))
        return id_no

    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data["is_superuser"]
        security_question = cleaned_data["security_question"]
        security_answer = cleaned_data["security_answer"]

        if not is_superuser:
            if not security_question:
                self.add_error(
                    "security_question",
                    _("Sequrity question is required for regular users."),
                )
            if not security_answer:
                self.add_error(
                    "security_answer",
                    _("Sequrity answer is required for regular users."),
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "id_no",
            "first_name",
            "middle_name",
            "last_name",
            "security_question",
            "security_answer",
            "is_active",
            "is_staff",
            "is_superuser",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email

    def clean_id_no(self):
        id_no = self.cleaned_data["id_no"]
        if User.objects.exclude(pk=self.instance.pk).filter(id_no=id_no).exists():
            raise ValidationError(_("A user with that ID number already exists."))
        return id_no

    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data["is_superuser"]
        security_question = cleaned_data["security_question"]
        security_answer = cleaned_data["security_answer"]

        if not is_superuser:
            if not security_question:
                self.add_error(
                    "security_question",
                    _("Sequrity question is required for regular users."),
                )
            if not security_answer:
                self.add_error(
                    "security_answer",
                    _("Sequrity answer is required for regular users."),
                )

        return cleaned_data
