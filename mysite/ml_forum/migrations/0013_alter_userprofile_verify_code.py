# Generated by Django 4.0.4 on 2022-04-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_forum', '0012_userprofile_verify_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='verify_code',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
