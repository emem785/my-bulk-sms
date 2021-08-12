from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Group


@receiver(signal=post_save, sender=Group)
def create_group(sender,instance,created,**kwargs):
	if created:
		print("group created")
