# Generated by Django 4.0.2 on 2022-02-25 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0064_scholar_app_sa_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholar_app',
            name='sa_path_to_pdf',
        ),
        migrations.RemoveField(
            model_name='scholar_info',
            name='si_path_to_pdf',
        ),
        migrations.RemoveField(
            model_name='scholar_info',
            name='si_photo_bg',
        ),
        migrations.RemoveField(
            model_name='scholar_news',
            name='sn_path_to_pdf',
        ),
        migrations.RemoveField(
            model_name='scholar_news',
            name='sn_photo_bg',
        ),
    ]
