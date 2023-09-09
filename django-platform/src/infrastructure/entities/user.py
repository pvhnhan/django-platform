from django.db import models
from .base import BaseEntity

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class UserEntity(BaseEntity):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)        
    avatar = models.FileField(upload_to=user_directory_path)

    class Meta:  
        db_table = "User"

    def __init__(self):
        pass
