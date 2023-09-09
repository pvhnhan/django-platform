from django.db import models
from .base import BaseEntity

class MediaEntity(BaseEntity):    
    name = models.CharField(max_length=100)
    name_upload = models.CharField(max_length=200)
    extension = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    path = models.CharField(max_length=500)    

    class Meta:  
        db_table = "Media"

    def __init__(self):
        pass