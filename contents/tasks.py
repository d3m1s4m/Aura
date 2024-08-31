import re
from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def process_post_content(post_id):
    """extract hashtags and mentions from the caption"""
    from .models import Post

    try:
        post = Post.objects.get(id=post_id)
        extract_hashtags(post)
        extract_mentions(post)
    except Post.DoesNotExist:
        pass


def extract_hashtags(post):
    from .models import Tag, PostTag

    tags = re.findall(r'#(\w+)', post.caption)
    for tag in tags:
        tag, created = Tag.objects.get_or_create(name=tag)
        PostTag.objects.get_or_create(post=post, tag=tag)


def extract_mentions(post):
    from .models import TaggedUser

    tagged_users = re.findall(r'@(\w+)', post.caption)
    for username in tagged_users:
        try:
            user = User.objects.get(username=username)
            TaggedUser.objects.get_or_create(post=post, user=user)
        except User.DoesNotExist:
            pass
