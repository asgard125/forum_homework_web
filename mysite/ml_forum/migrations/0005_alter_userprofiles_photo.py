# Generated by Django 4.0.4 on 2022-04-23 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_forum', '0004_rename_topic_posts_topic_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/'),
        ),
    ]
