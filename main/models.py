
from django.db import models
from django.db.models.base import Model
from main.helpers import helper_functions
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Tokens
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, username, password, first_name, last_name, phone_no, **other_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name,
                          last_name=last_name, phone_no=phone_no, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, first_name, last_name, phone_no, **other_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, username, password, first_name, last_name, phone_no, **other_fields)


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.PositiveIntegerField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no', 'username']

    objects = CustomUserManager()

    def __str__(self):
        return "{}".format(self.email)


# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     phone_no = models.PositiveIntegerField(unique=True)
#     email = models.EmailField(max_length=100, unique=True)
#     isemailverified = models.BooleanField(default=False)
#     joined_date = models.DateTimeField(auto_now_add=True)
#     password = models.CharField(max_length=50)

#     @staticmethod
#     def create_new_user(user, first_name, last_name, email, phone_no, password):
#         newUserProfile = UserProfile(
#             user=user,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             phone_no=phone_no,
#             password=password
#         )
#         newUserProfile.save()
#         return newUserProfile


# Create your models here.


class Customer(models.Model):
    # customer_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.PositiveIntegerField(unique=True)
    email = models.EmailField(max_length=100, unique=True)
    isemailverified = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.username} -- {self.id}'


class Message(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # Message_ID = models.IntegerField()
    message_content = models.TextField(max_length=2000)
    to = models.TextField()
    sender_name = models.CharField(max_length=200)
    message_status = models.CharField(max_length=50,)
    campaign_id = models.CharField(max_length=60)
    # campaign_id should be included
    campaign_name = models.CharField(max_length=60, blank=True, null=True)
    scheduled_for = models.DateField(blank=True, null=True)
    content = models.TextField(max_length=2000)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender_name)


class Group(models.Model):
    # group_Id= models.IntegerField(unique=True) unnecessary bcause django auto create id for every model
    # changed to name to avoid redundancy
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contact_sum = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_contact(self):
        return len(self.number).count()


class Contact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # contact = models.IntegerField() auto generated
    mobile_numbers = models.TextField()
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # transaction_id = models.IntegerField() autogenerated by django
    amount = models.IntegerField()
    unit = models.IntegerField()
    balance = models.IntegerField()
    tracking_code = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) and str(self.tracking_code)


class Template(models.Model):
    # template_id = models.IntegerField() #autogenerated by django
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content_message = models.TextField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date_created = models.DateTimeField(auto_now=True)


class Sender(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # _id = models.IntegerField() auto generated bydjango
    sender = models.OneToOneField(
        Message, on_delete=models.CASCADE, unique=True)  # Unique
    company_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
