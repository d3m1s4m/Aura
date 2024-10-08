# Generated by Django 4.2.15 on 2024-09-09 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Save'), (5, 'Mention'), (6, 'Accept request'), (7, 'Follow request'), (8, 'Unfollow'), (9, 'Reply')], verbose_name='notification type'),
        ),
    ]
