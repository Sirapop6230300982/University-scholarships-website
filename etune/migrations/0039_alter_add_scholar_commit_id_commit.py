# Generated by Django 4.0.1 on 2022-02-15 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('etune', '0038_remove_add_scholar_commit_scholar_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_scholar_commit',
            name='id_commit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
