from django.db import models
import re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name'])<2 or postData['name'].isalpha()==False:
            errors['name']='please enter a valid name'
        if len(postData['alias'])<2 or postData['alias'].isalpha()==False:
            errors['alias']='please enter a valid alias'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']='please enter a valid email'
        for user in User.objects.all():
            if user.email == postData['email']:
                errors['email_used']='email is already in DB'
        if len(postData['password'])<8:
            errors['password']='password must be at least 8 characters'
        if postData['password']!=postData['confirm']:
            errors['confirm']='confirmation password and password do not match'
        return errors
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(user)<1:
            errors['login_email']='that email is not registered'
        else:
            login_User=user[0]
            if not bcrypt.checkpw(postData['password'].encode(),login_User.password.encode()):
                errors['wrong_password']='password entered is incorrect'
        return errors

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title'])<2:
            errors['title']='please enter a valid title'
        return errors

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors ={}
        if len(postData['content'])<2:
            errors['content']='please enter a valid review'
        return errors

class Review(models.Model):
    content = models.TextField(blank=True)
    rating = models.IntegerField(null=True)
    by_user = models.ForeignKey(User, related_name= 'reviews', on_delete= models.CASCADE)
    for_book = models.ForeignKey(Book, related_name= 'reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()