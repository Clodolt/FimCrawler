# Generated by Django 3.0.7 on 2020-07-08 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_delete_journals'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='date_latest_issue',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='journal',
            name='issOld',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='journal',
            name='issue',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
