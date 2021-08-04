
from django.db import models
from django.db.models.base import Model
from main.helpers import helper_functions
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .manager import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    first_name    = models.CharField(_('first name'),max_length = 250)
    last_name    = models.CharField(_('last name'),max_length = 250)
    email         = models.EmailField(_('email'), unique=True)
    phone         = models.CharField(_('phone'), max_length = 20, unique = True)
    address       = models.CharField(_('address'), max_length = 250, null = True)
    password      = models.CharField(_('password'), max_length=300)
    is_staff      = models.BooleanField(_('staff'), default=False)
    is_admin      = models.BooleanField(_('admin'), default= False)
    is_active     = models.BooleanField(_('active'), default=True)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password', 'phone','first_name','last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email




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
