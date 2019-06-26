from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date, timedelta
# from apps.trip_buddy_app.models import Trip
import re
import bcrypt

class LoginManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # # first_name and last_name should be at least 2 characters
        # # email address should be valid
        # # passwords should match
        # # password should  be at least 8 characters
        # # add birthday field and validare that it is in the past
        # # password should be unique
        # # validae that the registered user is at least 13 years old
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'User first_name should be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'User last_name should be at least 2 characters'
        if self.isValidEmail(postData['email']) is False:
            errors['email'] = 'User email should be valid'
        if  self.email_unique(postData['email']) is False:
            errors['email'] = 'User email should be unique'
        if postData['birthday']:
            if not (self.birthday_in_past(postData['birthday']) and self.at_least_13(postData['birthday'])):
                errors['birthday'] = 'User birthday should be in the past and must be at least 13 years old'
        else:
            errors['birthday'] = 'User birthday should not be blank'
        if len(postData['password']) >= 8:
            if not (self.password_unique(postData['password'])):
                errors['password'] = 'User password should be at least 8 characters and be unique'
        else:
            errors['password'] = 'User password should be at least 8 characters and be unique'
        if postData['password'] != postData['confirm_pw']:
            errors['confirm'] = 'Confirm password must match User password'
        return errors

    def login_validator(self, postData):
        errors = {}
        if self.isValidEmail(postData['email']) != True :
            errors['email'] = 'User email should be valid'
        if len(postData['password']) < 8:
            errors['password'] = 'User password should be at least 8 characters'
        return errors

    def isValidEmail(self, email):
        if len(email) > 7:
            if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
                return True
        return False

    # def get_all_passwords(self):
    #     all_users = User.objects.all()
    #     passwords = []
    #     for user in all_users:
    #         passwords.append(user.password)
    #     return passwords

    def password_unique(self, item):
        all_users = User.objects.all()
        # item = bcrypt.hashpw(item.encode(), bcrypt.gensalt())
        for user in all_users:
            if bcrypt.checkpw(item.encode(), user.password.encode()):
                return False
        return True

    def email_unique(self, email):
        users = User.objects.all()
        for user in users:
            if email == user.email:
                return False
        return True

    def birthday_in_past(self, date):
        today = datetime.now()
        given_date = datetime.strptime(date, '%Y-%m-%d')
        if given_date < today:
            return True
        return False

    def at_least_13(self, birthday):
        today = datetime.now()
        user = datetime.strptime(birthday, '%Y-%m-%d')
        delta = today - user
        if delta > timedelta(days=4745):
            return True
        return False
        

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    password = models.CharField(max_length=255)
    # trips = models.ManyToManyField('trip_buddy_app.Trip', related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

    def __repr__(self):
        return f"first_name: {self.first_name}, last_name: {self.last_name}, email: {self.email}, birthday: {self.birthday}, created_at: {self.created_at}, updated_at: {self.updated_at}"