
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from main.helpers.helper_functions import (initial_bonus_sum,
                                           paystack_payment_request,
                                           unit_converter)
from main.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=250)
    last_name = models.CharField(_('last name'), max_length=250)
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(_('phone'), max_length=20, unique=True)
    address = models.CharField(_('address'), max_length=250, null=True)
    password = models.CharField(_('password'), max_length=300)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    firebase_key = models.CharField(
        _('firebase_key'), max_length=300, default="FBK")
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'firebase_key']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Message(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    user = models.EmailField(max_length=150)
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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    user = models.EmailField(max_length=150)
    contact_sum = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_contact(self):
        return len(self.number).count()


class Contact(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # contact = models.IntegerField() auto generated
    mobile_numbers = models.TextField()
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, related_name="contacts")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Balance(models.Model):
    user = models.EmailField(max_length=150)
    unit = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    @staticmethod
    def create_balance_first_time_user(user, unit, amount):
        first_time_user_balance = Balance(
            user=user,
            amount=amount,
            unit=unit
        )

        first_time_user_balance.save()

        return first_time_user_balance

    @staticmethod
    def update_user_balance(user, unit, amount):
        balance = Balance.objects.filter(user=user)
        updateBalance = balance.update(unit=unit, amount=amount)

        return updateBalance


class Payment_verification(models.Model):
    user = models.EmailField(max_length=150)
    payment_reference = models.CharField(max_length=50)
    reason = models.CharField(max_length=100)
    save_card = models.BooleanField(default=False)

    @staticmethod
    def paystack_request(user, user_ref, reason, savecard):
        paystack_response = paystack_payment_request(user_ref)

        if paystack_response.get("message") == "Verification successful":
            if savecard:
                # save to credit card detail

                card = paystack_response.get('data').get('authorization')
                card_exists = Credit_card_details.objects.filter(
                    card_signature=card.get('signature')).exists()
                if not card_exists:
                    Credit_card_details.create_credit_card(
                        user,
                        card.get('signature'),
                        card.get('account_name'),
                        card.get('bank'),
                        card.get('bin'),
                        card.get('last4'),
                        card.get('authorization_code'),
                        card.get('exp_month'),
                        card.get('exp_year'),
                        card.get('card_type'),
                        card.get('channel'),
                        card.get('country_code'),
                        card.get('brand'))

            # save to transaction table
            transact = paystack_response.get('data')
            unit = unit_converter(transact.get('amount'))
            amount = initial_bonus_sum(transact.get('amount'))
            PaymentTransaction.create_transaction(user, transact.get(
                'amount'), unit, transact.get('id'), reason, transact.get('reference'))

            try:
                userBal = Balance.objects.get(user=user)
                Balance.update_user_balance(
                    userBal, unit, transact.get('amount'))

            except Balance.DoesNotExist:
                Balance.create_balance_first_time_user(
                    user, unit, amount)

            message = {"status": "Payment successful"}
            return message

        else:
            return paystack_response


class PaymentTransaction(models.Model):

    user = models.EmailField(max_length=150)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    unit = models.DecimalField(decimal_places=2, max_digits=10)
    tracking_code = models.IntegerField()
    reason = models.CharField(max_length=100)
    tracking_ref = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) and str(self.tracking_code)

    @staticmethod
    def create_transaction(user, amount, unit, tracking_code, reason, tracking_ref):

        new_transcation = PaymentTransaction(
            user=user,
            amount=amount,
            unit=unit,
            tracking_code=tracking_code,
            reason=reason,
            tracking_ref=tracking_ref,
        )

        new_transcation.save()

        return new_transcation


class Template(models.Model):
    # template_id = models.IntegerField() #autogenerated by django
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    user = models.EmailField(max_length=150)
    title = models.CharField(max_length=100)
    content_message = models.TextField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date_created = models.DateTimeField(auto_now=True)


class Credit_card_details(models.Model):

    user = models.EmailField(max_length=150)
    card_signature = models.CharField(max_length=150)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(
        max_length=100, default="Invalid", blank=True)
    bin = models.CharField(max_length=6)
    card_last_four_digit = models.CharField(max_length=4)
    authorization_code = models.CharField(max_length=100)
    exp_month = models.CharField(max_length=2)
    exp_year = models.CharField(max_length=4)
    card_type = models.CharField(max_length=20)
    channel = models.CharField(max_length=20)
    country_code = models.CharField(max_length=20)
    brand = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) and str(self.card_signature)

    @staticmethod
    def create_credit_card(user="null", card_signature="null", account_name="invalid", bank_name="null", bin="null", card_last_four_digit="null", authorization_code="null",
                           exp_month="null", exp_year="null", card_type="null", channel="null", country_code="null", brand="null"):

        print(user)

        new_credit_card = Credit_card_details(
            user=user,
            card_signature=card_signature,
            bank_name=bank_name,
            account_name="invalid" if account_name is None else account_name,
            bin=bin,
            card_last_four_digit=card_last_four_digit,
            authorization_code=authorization_code,
            exp_month=exp_month,
            exp_year=exp_year,
            card_type=card_type,
            channel=channel,
            country_code=country_code,
            brand=brand
        )

        new_credit_card.save()

        return new_credit_card


class Sender(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    user = models.EmailField(max_length=150)
    # _id = models.IntegerField() auto generated bydjango
    sender = models.CharField(max_length=100, unique=True)  # Unique
    company_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
