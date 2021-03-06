# Generated by Django 4.0.1 on 2022-02-15 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('etune', '0031_scholar_app_add_scholar_commit'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholar_app',
            name='sa_userid',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scholar_app',
            name='sa_path_to_pdf',
            field=private_storage.fields.PrivateFileField(storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='scholar_app',
            name='sa_score',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='scholar_app',
            name='sa_sp_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='etune.scholar_profile'),
        ),
    ]
