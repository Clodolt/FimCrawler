# Generated by Django 3.0.7 on 2020-07-06 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200706_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='not_interested',
            field=models.ManyToManyField(to='core.Journal'),
        ),
    ]