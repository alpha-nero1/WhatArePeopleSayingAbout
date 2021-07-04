from django.db import models
from app.common.base_model import BaseModel
from app_auth.models import User
from app.models import Post

class Comment(BaseModel):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "comments"

class PostComment(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class CommentLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class CommentDislike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class PostLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class PostDislike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)