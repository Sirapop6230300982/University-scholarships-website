# Generated by Django 4.0.1 on 2022-02-13 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etune', '0029_alter_scholar_profile_sp_parttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar_profile',
            name='sp_father_title',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='scholar_profile',
            name='sp_mother_title',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='scholar_profile',
            name='sp_title_en',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='scholar_profile',
            name='sp_title_th',
            field=models.CharField(max_length=10, null=True),
        ),
    ]