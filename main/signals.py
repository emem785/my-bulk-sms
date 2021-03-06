from django.db.models.signals import post_save
from django.dispatch import receiver
from whisper.settings import cloud_messaging

from main.models import Group, PaymentTransaction, User


@receiver(signal=post_save, sender=Group)
def create_group(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(email=instance.user)
        token = user.firebase_key
        print(token)
        cloud_messaging.send_broadcast(
            token=token, title="Group", body="Group created")
        print("group created")


@receiver(signal=post_save, sender=PaymentTransaction)
def create_group(sender, instance: PaymentTransaction, created, **kwargs):
    if created:
        user = User.objects.get(email=instance.user)
        token = user.firebase_key
        data = {"reason": instance.reason, "amount": str(instance.amount),"time":str(instance.date_created)}
        cloud_messaging.send_broadcast(
            token=token, title="Transaction", body="Transaction completed", data=data)
        print("transaction created")
