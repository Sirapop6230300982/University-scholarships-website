# Generated by Django 4.0.1 on 2022-02-17 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('etune', '0045_alter_avatar_profile_sp_path_to_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar_profile',
            name='sa_userid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]