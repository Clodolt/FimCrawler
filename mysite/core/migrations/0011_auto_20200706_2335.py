# Generated by Django 3.0.7 on 2020-07-06 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200706_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='not_interested',
            field=models.ManyToManyField(blank=True, to='core.Journal'),
        ),
    ]
