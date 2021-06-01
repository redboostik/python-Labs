from django.db import models
from jsonfield import JSONField
# Create your models here.


class User(models.Model):
    telegram_id = models.PositiveIntegerField(
        verbose_name='user telegram ID',
        unique=True,
    )
    name=models.TextField(
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
    owner_ID = models.PositiveIntegerField(
        verbose_name='owner ID',
    )


    class Meta:
        verbose_name = 'Event model'
