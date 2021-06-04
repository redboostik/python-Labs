import threading
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from .commands import *
from .notifications import check_notifications


class Command(BaseCommand):
    help = 'tele bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=5,
            read_timeout=5,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            base_url=settings.PROXY_URL,
        )

        updater = Updater(
            bot=bot,
            use_context=True,
        )
        command_handler_create_event = CommandHandler('createevent', create_event)
        command_handler_my_id = CommandHandler('myid', my_id)
        command_handler_active_event = CommandHandler('activeevent', active_event)
        command_handler_open_event = CommandHandler('openevent', open_event)
        command_handler_close_event = CommandHandler('closeevent', close_event)
        command_handler_delete_event = CommandHandler('deleteevent', delete_event)
        command_handler_set_name = CommandHandler('setname', set_name)
        command_handler_set_description = CommandHandler('setdescription', set_description)
        command_handler_set_datetime = CommandHandler('setdatetime', set_datetime)
        command_handler_add_subscriber = CommandHandler('addsubscribers', add_subscribers)
        command_handler_delete_subscriber = CommandHandler('deletesubscribers', delete_subscribers)
        command_handler_view_active_event = CommandHandler('viewactiveevent', view_active_event)
        command_handler_view_my_events = CommandHandler('viewmyevents', view_my_events)
        command_handler_view_my_notifications = CommandHandler('viewmynotifications', view_my_notifications)
        command_handler_set_datetime_notification_by_id = CommandHandler('setdatetimenotificationbyid',
                                                                         set_datetime_notification_by_id)
        command_handler_set_title_notification_by_id = CommandHandler('settitlenotificationbyid',
                                                                      set_title_notification_by_id)
        message_handler_commands = MessageHandler(Filters.text, message_handler)
        self.run_checker()
        updater.dispatcher.add_handler(command_handler_create_event)
        updater.dispatcher.add_handler(command_handler_my_id)
        updater.dispatcher.add_handler(command_handler_active_event)
        updater.dispatcher.add_handler(command_handler_open_event)
        updater.dispatcher.add_handler(command_handler_close_event)
        updater.dispatcher.add_handler(command_handler_delete_event)
        updater.dispatcher.add_handler(command_handler_set_name)
        updater.dispatcher.add_handler(command_handler_set_description)
        updater.dispatcher.add_handler(command_handler_set_datetime)
        updater.dispatcher.add_handler(command_handler_add_subscriber)
        updater.dispatcher.add_handler(command_handler_delete_subscriber)
        updater.dispatcher.add_handler(command_handler_view_active_event)
        updater.dispatcher.add_handler(command_handler_view_my_events)
        updater.dispatcher.add_handler(command_handler_view_my_notifications)
        updater.dispatcher.add_handler(command_handler_set_datetime_notification_by_id)
        updater.dispatcher.add_handler(command_handler_set_title_notification_by_id)
        updater.dispatcher.add_handler(message_handler_commands)
        updater.start_polling()
        updater.idle()

    @staticmethod
    def run_checker():
        th = threading.Thread(group=None, target=check_notifications,
                              name='Checker', args=(),
                              kwargs={}, daemon=None)
        th.start()
