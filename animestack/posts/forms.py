from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    # text = forms.CharField(label="Введите текст", widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ("text", "group")
