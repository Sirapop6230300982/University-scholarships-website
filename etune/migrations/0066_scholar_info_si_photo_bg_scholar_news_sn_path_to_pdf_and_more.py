# Generated by Django 4.0.2 on 2022-02-25 05:21

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0065_remove_scholar_app_sa_path_to_pdf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholar_info',
            name='si_photo_bg',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], default=1, force_format=None, keep_meta=True, quality=100, size=[1280, 720], upload_to='uploads/info'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scholar_news',
            name='sn_path_to_pdf',
            field=models.FileField(default=1, upload_to='documents/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scholar_news',
            name='sn_photo_bg',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], default=1, force_format=None, keep_meta=True, quality=100, size=[1280, 720], upload_to='uploads/'),
            preserve_default=False,
        ),
    ]
