from django import forms
from .models import BlogItems, BlogComment


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
    

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogItems
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
