# Generated by Django 3.2.3 on 2021-06-03 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rb_planner_bot', '0010_auto_20210603_0001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={'verbose_name': 'Notification'},
        ),
        migrations.AddField(
            model_name='notifications',
            name='title',
            field=models.TextField(default='title', verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 4, 0, 14, 10, 635409), verbose_name='event start date'),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 4, 0, 14, 10, 636263), verbose_name='notification date'),
        ),
    ]