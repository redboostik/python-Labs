from django.core.management.base import BaseCommand
from django.conf import settings
from rb_planner_bot.models import *
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.utils.request import Request


def send_text(update: Update, text: str):
    update.message.reply_text(
        text=text,
    )


def create_event(update: Update, context: CallbackContext):
    update_user(update)
    event = Event.objects.create(
        owner_ID=update.message.chat_id,
        name='Event',
        description='description',
        subscribers=[],
    )
    __open_event(update, event.id)

    ans = 'Event successfully created\n Event id: {}'.format(event.id)
    send_text(update, ans)


def my_id(update: Update, context: CallbackContext):
    update_user(update)
    ans = 'Your ID: {}\n Your username: {}\n'.format(update.message.chat_id, update.message.from_user.username)
    send_text(update, ans)


def active_event(update: Update, context: CallbackContext):
    update_user(update)
    aevent = ActiveEvents.objects.get(owner_ID=update.message.chat_id)
    event = Event.objects.get(id=aevent.event_ID)
    ans = 'Active event \nname: {}\n id: {}'.format(event.name, event.id)
    send_text(update, ans)


def close_event(update: Update, context: CallbackContext):
    update_user(update)
    ActiveEvents.objects.get_or_create(owner_ID=update.message.chat_id)[0].delete()
    send_text(update, 'event closed')


def open_event(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "openevent")
    send_text(update, 'Enter event id')


def delete_event(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "deleteevent")
    send_text(update, 'Enter event id')


def __open_event(update: Update, event_id):
    ActiveEvents.objects.update_or_create(
        owner_ID=update.message.chat_id,
        defaults={
            'event_ID': event_id
        }
    )


def add_command(update: Update, command: str):
    an, _ = ActiveCommand.objects.update_or_create(
        user_ID=update.message.chat_id,
        defaults={
            'command': command
        }
    )


def update_user(update: Update):
    User.objects.update_or_create(
        telegram_id=update.message.chat_id,
        defaults={
            'name': update.message.from_user.username if update.message.from_user.username is not None else 'None',
        }
    )


def set_name(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "setname")
    send_text(update, 'Enter event name')


def set_description(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "setdescription")
    send_text(update, 'Enter event description')


def set_datetime(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "setdatetime")
    send_text(update, 'Enter event (format: "day-month-year-hours-minutes"))')


def add_subscribers(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "addsubscribers")
    send_text(update, 'Enter subscriber id')


def delete_subscribers(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "deletesubscribers")
    send_text(update, 'Enter subscriber id')


def message_handler(update: Update, context: CallbackContext):
    update_user(update)
    text = update.message.text
    act_event = ActiveEvents.objects.get(owner_ID=update.message.chat_id)
    active_command = ActiveCommand.objects.get(user_ID=update.message.chat_id)

    if active_command.command == 'openevent':
        __open_event(update, int(text))
        send_text(update, 'event opened')

    elif active_command.command == 'deleteevent':
        Event.objects.get(id=int(text)).delete()
        send_text(update, 'event deleted')

    elif active_command.command == 'setname':
        event = Event.objects.get(id=act_event.event_ID)
        event.name = text
        event.save()
        send_text(update, 'event name updated')

    elif active_command.command == 'setdescription':
        event = Event.objects.get(id=act_event.event_ID)
        event.description = text
        event.save()
        send_text(update, 'event description updated')
    elif active_command.command == 'setdatetime':
        event = Event.objects.get(id=act_event.event_ID)
        event.date = datetime.datetime.strptime(text, '%d-%m-%Y-%H-%M')
        event.save()
        send_text(update, 'event datetime updated')
    elif active_command.command == 'addsubscribers':
        event = Event.objects.get(id=act_event.event_ID)
        event.subscribers.append(text)
        event.save()
        send_text(update, 'added subscriber')
    elif active_command.command == 'deletesubscribers':
        event = Event.objects.get(id=act_event.event_ID)
        event.subscribers.remove(text)
        event.save()
        send_text(update, 'subscriber deleted')


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
        message_handler_commands = MessageHandler(Filters.text, message_handler)

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
        updater.dispatcher.add_handler(message_handler_commands)

        updater.start_polling()
        updater.idle()
