# Generated by Django 4.0.1 on 2022-02-04 15:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('etune', '0017_scholar_profile_delete_scholar_profile2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Scholar_profile',
            new_name='Scholar_profile2',
        ),
    ]