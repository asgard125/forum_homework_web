# Generated by Django 4.0.4 on 2022-04-24 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_forum', '0006_remove_topics_start_post_id_topics_start_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topics',
            name='start_post',
        ),
        migrations.AddField(
            model_name='posts',
            name='start_post',
            field=models.BooleanField(default=False),
        ),
    ]
