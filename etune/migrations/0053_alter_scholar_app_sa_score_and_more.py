# Generated by Django 4.0.1 on 2022-02-18 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0052_remove_scholar_app_sa_sp_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar_app',
            name='sa_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scholar_app',
            name='sa_score_info',
            field=models.JSONField(null=True),
        ),
    ]
