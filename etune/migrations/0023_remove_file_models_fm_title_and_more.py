# Generated by Django 4.0.1 on 2022-02-08 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0022_alter_scholar_info_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file_models',
            name='fm_title',
        ),
        migrations.RemoveField(
            model_name='scholar_info',
            name='si_sub_type',
        ),
    ]
