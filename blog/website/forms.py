from django import forms
from .models import BlogItems


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = BlogItems
        fields = ["title", "content"]
