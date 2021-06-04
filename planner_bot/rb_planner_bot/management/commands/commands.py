from rb_planner_bot.models import *
from telegram import Update
from telegram.ext import CallbackContext
from .notifications import send_message
import re


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
        subscribers=[update.message.chat_id],
        date=datetime.datetime.today() + datetime.timedelta(days=1)
    )
    __open_event(update, event.id)
    __create_notification(event, update.message.chat_id)

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


def view_active_event(update: Update, context: CallbackContext):
    update_user(update)
    event_id = ActiveEvents.objects.get(owner_ID=update.message.chat_id).event_ID
    event = Event.objects.get(id=event_id)
    send_text(update, event.name + '\n\n' + event.description + '\n\n' + event.date.strftime('%d-%m-%Y-%H-%M')
              + '\n\n' + str(event.subscribers))


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
    send_text(update, 'Enter datetime (format: "day-month-year-hours-minutes"))')


def add_subscribers(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "addsubscribers")
    send_text(update, 'Enter subscriber id')


def delete_subscribers(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "deletesubscribers")
    send_text(update, 'Enter subscriber id')


def __delete_notification(event: Event, user_id: int):
    Notifications.objects.get(
        owner_ID=user_id,
        event_ID=event.id,
    ).delete()


def __create_notification(event: Event, user_id: int):
    Notifications.objects.update_or_create(
        owner_ID=user_id,
        event_ID=event.id,
        defaults={
            'title': event.name,
            'date': event.date
        }
    )


def view_my_events(update: Update, context: CallbackContext):
    update_user(update)
    ans = ''
    for event in Event.objects.filter(owner_ID=update.message.chat_id):
        ans += str(event.id) + '\n' + event.name + '\n' + event.description + '\n' + \
               event.date.strftime('%d-%m-%Y-%H-%M') + '\n' + str(event.subscribers) + '\n\n'
    send_text(update, ans)


def view_my_notifications(update: Update, context: CallbackContext):
    update_user(update)
    ans = ''
    for notif in Notifications.objects.filter(owner_ID=update.message.chat_id):
        event = Event.objects.get(id=notif.event_ID)
        ans += str(notif.id) + '\n' + notif.title + '\n' + event.name + '\n' + event.description + '\n' \
                   + notif.date.strftime('%d-%m-%Y-%H-%M') + '\n' + '\n\n '
    send_text(update, ans)


def set_datetime_notification_by_id(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "setdatetimenotificationbyid")
    ans = 'Enter notification id and datetime (format: "day-month-year-hours-minutes"))'
    send_text(update, ans)


def set_title_notification_by_id(update: Update, context: CallbackContext):
    update_user(update)
    add_command(update, "settitlenotificationbyid")
    ans = 'Enter notification id and title'
    send_text(update, ans)


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
        for item in Notifications.objects.filter(event_ID=event.id):
            send_message(item.owner_ID,
                         "Notification {}\nEvent date '{}' changed\n{}".format(item.title, event.name, str(event.date)))
    elif active_command.command == 'addsubscribers':
        event = Event.objects.get(id=act_event.event_ID)
        event.subscribers.append(int(text))
        __create_notification(event, int(text))
        send_message(int(text), 'You added to event "{}"'.format(event.name))
        event.save()
        send_text(update, 'added subscriber')
    elif active_command.command == 'deletesubscribers':
        event = Event.objects.get(id=act_event.event_ID)
        event.subscribers.remove(int(text))
        __delete_notification(event, int(text))
        send_message(int(text), 'You was deleted from event "{}"'.format(event.name))
        event.save()
        send_text(update, 'subscriber deleted')
    elif active_command.command == 'setdatetimenotificationbyid':
        reg = re.match('(\d+) (\S+)', text, )
        notif = Notifications.objects.get(id=int(reg[1]))
        notif.date = datetime.datetime.strptime(str(reg[2]), '%d-%m-%Y-%H-%M')
        notif.save()
        send_text(update, 'notification datetime updated')
    elif active_command.command == 'settitlenotificationbyid':
        reg = re.match('(\d+) (\S+)', text)
        notif = Notifications.objects.get(id=int(reg[1]))
        notif.title = str(reg[2])
        notif.save()
        send_text(update, 'notification title updated')
