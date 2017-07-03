from django import forms
from django_summernote.widgets import SummernoteWidget
from taggit.forms import TagField

from .models import Post


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    tags = TagField(required=False)

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]

        widgets = {
            "content": SummernoteWidget()
        }
