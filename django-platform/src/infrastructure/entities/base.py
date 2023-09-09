import uuid
from django.db import models

class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField()
    created_by = models.CharField(max_length=50)
    updated_date = models.DateField()
    updated_by = models.CharField(max_length=50)

    class Meta:
        abstract = True
