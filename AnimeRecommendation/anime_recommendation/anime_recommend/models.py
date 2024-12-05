from django.db import models
from django.contrib.auth.models import AbstractUser , Group , Permission
# Create your models here.

class User(AbstractUser):
    anime_liking = models.JSONField(default=dict)
    anime_watched = models.JSONField(default=list)
    groups = models.ManyToManyField(Group,related_name="custom_user_set",blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name="custom_user_permission_set",blank=True)

class anime_data(models.Model):
    anime_id = models.IntegerField(unique=True)
    title = models.TextField(max_length=255)
    genre = models.JSONField()
    popularity = models.IntegerField()
    description = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



