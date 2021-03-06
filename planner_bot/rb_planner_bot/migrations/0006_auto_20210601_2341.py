# Generated by Django 3.2.3 on 2021-06-01 23:41

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rb_planner_bot', '0005_user_telegram_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_ID', models.PositiveIntegerField(verbose_name='owner ID')),
                ('event_ID', models.PositiveIntegerField(verbose_name='event ID')),
            ],
            options={
                'verbose_name': 'Active event',
            },
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event model'},
        ),
        migrations.AlterField(
            model_name='event',
            name='subscribers',
            field=jsonfield.fields.JSONField(default=dict, verbose_name='subscribers IDs'),
        ),
    ]
