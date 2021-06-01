from django.core.management.base import BaseCommand
from django.conf import settings
from rb_planner_bot.models import *
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request


def write_ans(update: Update, context: CallbackContext):
    __update_user(update)
    chat_id = update.message.chat_id
    text = update.message.text
    ans = "your's ID {}\nText\n{}".format(chat_id, text)
    update.message.reply_text(
        text=ans,
    )


def command_parser(update: Update, context: CallbackContext):
    __update_user(update)
    text = update.message.text
    if text == '/start':
        name = update.message.from_user.username
        ans = 'start command. your username is {} '.format(name)
        update.message.reply_text(
            text=ans,
        )


def __update_user(update: Update):
    User.objects.get_or_create(
        telegram_id=update.message.chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )


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

        message_handler_start = MessageHandler(Filters.command, command_parser)
        message_handler_text = MessageHandler(Filters.text, write_ans)
        updater.dispatcher.add_handler(message_handler_start)
        updater.dispatcher.add_handler(message_handler_text)

        updater.start_polling()
        updater.idle()
