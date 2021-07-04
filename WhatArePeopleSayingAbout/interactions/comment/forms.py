from app_auth.models import User
from django import forms
from django.db import models
from ..models import Comment

class CreatePostCommentForm(forms.ModelForm):
    post_uuid = models.CharField()
    parent_id = models.IntegerField(blank=True)
    text = models.CharField(max_length=255)

    ## all the fields deeming the form valid
    class Meta:
        model = Comment

        fields = (
            'text',
        )

class DeletePostCommentForm(forms.ModelForm):
    ## all the fields deeming the form valid
    class Meta:
        model = Comment

        fields = (
            'id',
        )