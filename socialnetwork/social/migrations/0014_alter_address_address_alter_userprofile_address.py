# Generated by Django 4.0.5 on 2022-06-30 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0013_remove_userprofile_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='social.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]