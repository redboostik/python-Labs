from django.conf import settings
from telegram import Bot
from telegram.utils.request import Request
from .commands import *
from datetime import timezone
import json

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
    bot.request


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
            for item in json.loads(event.subscribers[1:-1]):
                print(item)
                send_message(int(item),
                             'event starting now\n\n{}\n{}\n{}\n'.format(event.name, event.description, str(event.date)))
            Event.objects.get(id=event.id).delete()

