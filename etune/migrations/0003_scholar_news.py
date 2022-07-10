# Generated by Django 4.0.1 on 2022-01-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0002_mymodel_upload_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scholar_news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sn_header', models.CharField(max_length=256)),
                ('sn_description', models.TextField()),
                ('sn_expire_date', models.DateField()),
                ('sn_photo_bg', models.ImageField(upload_to='uploads/')),
                ('sn_path_to_pdf', models.FileField(upload_to='documents/')),
            ],
        ),
    ]