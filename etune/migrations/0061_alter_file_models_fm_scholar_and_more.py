# Generated by Django 4.0.2 on 2022-02-23 17:22

from django.db import migrations, models
import django.db.models.deletion
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0060_alter_file_models_fm_scholar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_models',
            name='fm_Scholar',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='etune.scholar_info'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='file_models',
            name='fm_file',
            field=private_storage.fields.PrivateFileField(blank=True, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='', verbose_name='File'),
        ),
    ]
