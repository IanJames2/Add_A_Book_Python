from django.db import models
from django.core.validators import validate_email
from datetime import datetime
from time import strftime
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator_reg(self, post_data):
        errors = {}
        if len(post_data["first_name"]) < 2:
            errors["first_name"] = "Please enter at least 2 characters for your first name!"
        if len(post_data["last_name"]) < 2:
            errors["last_name"] = "Please enter at least 2 characters for your last name!"

        try:
            validate_email(post_data["email"])
        except:
            errors["email"] = "Please enter a valid email!"

        if len(post_data["password"]) < 8:
            errors["password"] = "Please enter a password of at least 8 characters!"
        if post_data["password"] != post_data["confirm"]:
            errors["confirm"] = "Please ensure your password matches the confirmation!"
        return errors
    
    def basic_validator_log(self, post_data):
        errors = {}
        same_email = User.objects.filter(email=post_data['email'])
        print("PRINTING MATCHING EMAIL HERE", same_email)
        if len(same_email) == 0:
            errors['emailnotfound'] = "This email is not found. Please register first." 
        # elif same_email[0].password != post_data['password']:
        #     errors['pwIncorrect'] = 'Incorrect Password'
        else: 
            if len(post_data['password']) > 0:
                user = User.objects.filter(email = post_data['email'])
                if user:
                    logged_user = user[0]
                    if not bcrypt.checkpw(post_data['password'].encode(), logged_user.password.encode()):
                        errors['password'] = "invalid login"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"<User object: {self.first_name} {self.last_name} {self.email} ({self.id})>"


class BookManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data["title"]) < 1:
            errors["title"] = "Please enter a title!"
        elif len(post_data["title"]) < 2:
            errors["title"] = "Please enter a title of at least 2 characters!"
        if len(post_data["description"]) < 1:
            errors["description"] = "Please provide a description!"
        elif len(post_data["description"]) < 2:
            errors["description"] = "Please enter at least 2 characters for the description!"

        return errors

class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    uploaded_by = models.ForeignKey(User, related_name = "books_uploaded", on_delete=models.CASCADE) #ManyToMany not required for object creation
    users_who_favorited = models.ManyToManyField(User, related_name="readers") #ForeignKey required for object creation unless null=True is apart of field.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()
    
    def __str__(self):
        return f"<Book object: {self.title} ({self.id})>"

