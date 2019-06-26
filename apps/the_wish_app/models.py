from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date, timedelta
# from apps.trip_buddy_app.models import Trip
import re
import bcrypt

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        # # item and last_name should be at least 3 characters
        # # description should  be at least 8 characters
        if len(postData['item']) < 3:
            errors['item'] = 'Wish item should be at least 3 characters'
        if len(postData['description']) < 3:
            errors['description'] = 'Wish description should be at least 3 characters'
        return errors

class LikeManager(models.Manager):
    def like_validator(self, postData):
        errors = {}
        # only allow the user to like an item once.
        if self.liked_wishes_by_userid(postData['wish_id'], postData['user_id']) >= 1:
            errors['like'] = 'A User can only like an item once'
        return errors

    def liked_wishes_by_userid(self, wish_id, user_id):
        return len(Like.objects.all().filter(wish_id=wish_id, user_id=user_id))

# Create your models here.
class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    date_granted = models.DateTimeField(null=True)
    user_id = models.IntegerField()
    granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

    def __repr__(self):
        return f"item: {self.item}, description: {self.description}, date_added: {self.date_added}, date_granted: {self.date_granted}, created_at: {self.created_at}, updated_at: {self.updated_at}, 'user_id': {self.user_id}, 'granted': {self.granted} "


class Like(models.Model):
    wish_id = models.IntegerField()
    user_id = models.IntegerField()
    objects = LikeManager()