from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    disabled_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True
