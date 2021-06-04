from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from .commands import *
from datetime import timezone

request = Request(
    connect_timeout=5,
    read_timeout=5,
)
bot = Bot(
        request=request,
        token=settings.TOKEN,
        base_url=settings.PROXY_URL,
    )


def send_message(user_id: int, message: str):
    bot.sendMessage(str(user_id), message)


def check_notifications():
    while True:
        notif = Notifications.objects.order_by('date').first()
        if notif is not None and notif.date <= datetime.datetime.now(timezone.utc):
            event = Event.objects.get(id=notif.event_ID)
            Notifications.objects.get(id=notif.id).delete()
            send_message(notif.owner_ID,
                         'event {} starting soon\n\n{}\n{}\n{}\n'.format(notif.title, event.name,
                                                                         event.description, str(event.date)))
        event = Event.objects.order_by('date').first()
        if event is not None and event.date <= datetime.datetime.now(timezone.utc):
            Event.objects.get(id=event.id).delete()
            send_message(event.owner_ID,
                         'event starting now\n\n{}\n{}\n{}\n'.format(event.name, event.description, str(event.date)))
