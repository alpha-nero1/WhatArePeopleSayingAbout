# Create your models here.
from django.db import models
import uuid
from app_auth.models import User
from .common.base_model import BaseModel

class Topic(BaseModel):
    name = models.CharField(max_length=255)
    kebab_name = models.CharField(max_length=255, unique=True)

class Post(BaseModel):
    text = models.CharField(max_length=1000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)