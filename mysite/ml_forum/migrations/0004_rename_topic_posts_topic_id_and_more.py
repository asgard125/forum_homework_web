# Generated by Django 4.0.4 on 2022-04-23 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ml_forum', '0003_rename_message_posts_post_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='topic',
            new_name='topic_id',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='topics',
            old_name='section',
            new_name='section_id',
        ),
        migrations.RenameField(
            model_name='topics',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='userprofiles',
            old_name='user',
            new_name='user_id',
        ),
    ]
