# Generated by Django 4.0.5 on 2022-07-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0019_alter_userprofile_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
