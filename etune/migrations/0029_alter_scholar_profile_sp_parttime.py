# Generated by Django 4.0.1 on 2022-02-13 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0028_alter_scholar_profile_sp_child_in_the_patron_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar_profile',
            name='sp_parttime',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
