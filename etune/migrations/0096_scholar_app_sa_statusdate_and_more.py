# Generated by Django 4.0.2 on 2022-03-09 15:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0095_scholar_info_si_endtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholar_app',
            name='sa_statusDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='scholar_app',
            name='sa_statusExDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
