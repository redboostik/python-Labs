import datetime

from django.db import models
from jsonfield import JSONField


class User(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name='user telegram ID',
        unique=True,
    )
    name = models.TextField(
        verbose_name='user full name',
    )

    class Meta:
        verbose_name = 'User model'


class Event(models.Model):
    name = models.TextField(
        verbose_name='event name',
    )
    description = models.TextField(
        verbose_name='event description',
    )

    subscribers = JSONField(
        verbose_name='subscribers IDs',
    )

    date = models.DateTimeField(
        verbose_name='event start date',
        default=datetime.datetime.today() + datetime.timedelta(days=1)
    )

    owner_ID = models.PositiveIntegerField(
        verbose_name='owner ID',
    )

    class Meta:
        verbose_name = 'Event model'


class ActiveEvents(models.Model):
    owner_ID = models.PositiveIntegerField(
        verbose_name='owner ID',
    )

    event_ID = models.PositiveIntegerField(
        verbose_name='event ID',
    )

    class Meta:
        verbose_name = 'Active event'


class ActiveCommand(models.Model):
    user_ID = models.PositiveIntegerField(
        verbose_name='user ID',
    )
    command = models.TextField(
        verbose_name='last command'
    )


class Notifications(models.Model):

    title = models.TextField(
        verbose_name='title',
        default='title'
    )

    owner_ID = models.PositiveIntegerField(
        verbose_name='owner ID',
    )

    event_ID = models.PositiveIntegerField(
        verbose_name='event ID',
    )

    date = models.DateTimeField(
        verbose_name='notification date',
        default=datetime.datetime.today() + datetime.timedelta(days=1)
    )

    class Meta:
        verbose_name = 'Notification'
