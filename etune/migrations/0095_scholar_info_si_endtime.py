# Generated by Django 4.0.2 on 2022-03-04 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0094_alter_scholar_info_si_source_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholar_info',
            name='si_endtime',
            field=models.DateField(blank=True, null=True),
        ),
    ]
