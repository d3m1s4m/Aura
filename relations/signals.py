from django.db.models.signals import post_save
from django.dispatch import receiver

from relations.models import BlockRelation, FollowRelation


@receiver(post_save, sender=BlockRelation)
def delete_follow_on_block(sender, instance, created, **kwargs):
    if created:
        # delete any follow relations involving the blocker and blocked user
        FollowRelation.objects.filter(from_user=instance.blocker, to_user=instance.blocked).delete()
        FollowRelation.objects.filter(from_user=instance.blocked, to_user=instance.blocker).delete()
