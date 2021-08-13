from django.db.models.signals import post_save
from django.dispatch import receiver
from whisper.settings import cloud_messaging

from main.models import Group, User


@receiver(signal=post_save, sender=Group)
def create_group(sender,instance,created,**kwargs):
	if created:
		user = User.objects.get(email=instance.user)
		token = user.firebase_key
		print(token)
		cloud_messaging.send_broadcast(token=token,title="Group",body="Group created")
		print("group created")
