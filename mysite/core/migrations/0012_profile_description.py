# Generated by Django 3.0.7 on 2020-07-06 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200706_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
