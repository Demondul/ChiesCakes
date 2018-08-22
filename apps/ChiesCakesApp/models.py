from __future__ import unicode_literals
from django.db import models

import bcrypt
import re

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX=re.compile(r'^[a-zA-Z\s]$')

class ValidationManager(models.Manager):
    def registration_validator(self, postData):
        errors={}
        if len(postData['txtFirst'])<1 or NAME_REGEX.match(postData['txtFirst']):
            errors['fName']="First name should be letters only."
        if len(postData['txtLast'])<1 or NAME_REGEX.match(postData['txtLast']):
            errors['lName']="Last name should be letters only."
        if not EMAIL_REGEX.match(postData['txtEmail']):
            errors['eMail']="Invalid eMail address."
        if len(postData['txtPWord'])<8 and len(postData['txtPWord'])>25:
            errors['pwLen']="Password should be atleast 8 and not more than 25 characters."
        if postData['txtPWord'] != postData['txtConWord']:
            errors['pwMatch']="Passwords did not match."
        return errors
    
    def login_validator(self,postData):
        validator={}
        users=Users.objects.filter(email_address=postData['txtUMail'])
        match=False
        if len(users)>0:
            for user in users:
                if bcrypt.checkpw(postData['txtUPWord'].encode(),user.password.encode()):
                    match=True
                    validator['match']=match
                    validator['ID']=user.id
            if not match:
                validator['noMatch']="eMail and password did not match."
        else:
            validator['noEmail']="eMail does not exist."
        return validator

    def review_validator(self,postData):
        errors={}
        if len(postData['txtReview']) < 10:
            errors['review']="Please tell me more about your cake experience."
        elif int(postData['hdnRating']) == 0:
            errors['rating']="Don't forget to rate the cake."
        return errors

# Create your models here.
class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.CharField(max_length=255)
    password=models.CharField(max_length=25)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ValidationManager()

class Reservations(models.Model):
    eventType=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    event_date=models.DateTimeField(editable=True)
    event_by=models.ForeignKey(Users,related_name="reserves", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ValidationManager()

class Orders(models.Model):
    orderType=models.CharField(max_length=255)
    description=models.TextField()
    quantity=models.IntegerField(default=1)
    celebrant=models.CharField(max_length=255)
    order_by=models.ForeignKey(Users,related_name="orders", on_delete=models.CASCADE)
    event=models.ForeignKey(Reservations,related_name="orders", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ValidationManager()

class Reviews(models.Model):
    # title=models.CharField(max_length=255)
    img_url=models.TextField()
    review=models.TextField()
    rating=models.IntegerField(default=5)
    review_by=models.ForeignKey(Users,related_name="my_reviews", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ValidationManager()

class Comments(models.Model):
    comment=models.TextField()
    comment_by=models.ForeignKey(Users,related_name="my_comments", on_delete=models.CASCADE)
    comment_in=models.ForeignKey(Reviews,related_name="the_comments", on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ValidationManager()

class Flavors(models.Model):
    flavor=models.TextField()
    img_url=models.CharField(max_length=255)