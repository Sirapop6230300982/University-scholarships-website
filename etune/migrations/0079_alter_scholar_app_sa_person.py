# Generated by Django 4.0.2 on 2022-02-26 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0078_rename_score_log_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar_app',
            name='sa_person',
            field=models.IntegerField(default=1),
        ),
    ]