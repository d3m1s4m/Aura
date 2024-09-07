from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from contents.models import TaggedUser
from notifications.models import Notification
from activities.models import Like, Comment, Save
from relations.models import FollowRelation


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.user,
            notification_type=Notification.LIKE,
            post=instance.post
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.user,
            notification_type=Notification.COMMENT,
            post=instance.post
        )


@receiver(post_save, sender=Save)
def create_save_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.user,
            notification_type=Notification.SAVE,
            post=instance.post
        )


@receiver(post_save, sender=FollowRelation)
def create_follow_request_notification(sender, instance, created, **kwargs):
    if created and not instance.is_accepted:
        Notification.objects.create(
            sender=instance.from_user,
            receiver=instance.to_user,
            notification_type=Notification.FOLLOW_REQUEST,
        )


@receiver(post_save, sender=FollowRelation)
def create_follow_notification(sender, instance, created, **kwargs):
    if instance.is_accepted:
        Notification.objects.create(
            sender=instance.from_user,
            receiver=instance.to_user,
            notification_type=Notification.FOLLOW,
        )


@receiver(post_save, sender=FollowRelation)
def create_accept_request_notification(sender, instance, created, **kwargs):
    # if user page is public, don't send this notification
    tolerance = timedelta(milliseconds=1)
    if abs(instance.created_at - instance.modified_at) <= tolerance:
        return

    if instance.is_accepted:
        Notification.objects.create(
            sender=instance.to_user,
            receiver=instance.from_user,
            notification_type=Notification.ACCEPT_REQUEST,
        )


@receiver(post_save, sender=TaggedUser)
def create_mention_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            sender=instance.post.user,
            receiver=instance.user,
            notification_type=Notification.MENTION,
            post=instance.post
        )


@receiver(post_save, sender=Comment)
def create_comment_reply_notification(sender, instance, created, **kwargs):
    if created and instance.reply_to:
        Notification.objects.create(
            sender=instance.user,
            receiver=instance.reply_to.user,
            notification_type=Notification.REPLY,
            post=instance.post
        )