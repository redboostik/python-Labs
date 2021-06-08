import telegram
from django.test import TestCase
from telegram.ext import Dispatcher
from telegram import Chat, Message
from rb_planner_bot.management.commands.commands import *
from django.conf import settings
from telegram import Bot
from telegram.utils.request import Request

request = Request(
    connect_timeout=5,
    read_timeout=5,
)
bot = Bot(
    request=request,
    token=settings.TOKEN,
    base_url=settings.PROXY_URL,
)
user = telegram.User(id=1, is_bot=False, first_name='test')
chat = Chat(1, 'private')
message = Message(1, 1, chat, user)
update = Update(1, message)
dispatcher = Dispatcher(bot, [])
call_back_context = CallbackContext(dispatcher)
test()


class TestCommands(TestCase):

    def test_create_event(self):
        ans = create_event(update, call_back_context)
        self.assertTrue(re.search(' id: (\d+)', ans, re.MULTILINE)[1] is not None, 'event not created')

    def test_active_event(self):
        create_event(update, call_back_context)
        ans = active_event(update, call_back_context)
        self.assertTrue(re.search(' id: (\d+)', ans, re.MULTILINE)[1] == '1')

    def test_view_my_events(self):
        create_event(update, call_back_context)
        create_event(update, call_back_context)
        ans = view_my_events(update, call_back_context)
        reg = re.findall('^(\d+)$', ans, re.MULTILINE)
        self.assertTrue(reg[0] == '1' and reg[1] == '2')

    def test_delete_event(self):
        ans = view_my_events(update, call_back_context)
        before = len(re.findall('^(\d+)$', ans, re.MULTILINE))
        create_event(update, call_back_context)
        delete_event(update, call_back_context)
        update.message.text = '1'
        message_handler(update,call_back_context)
        ans = view_my_events(update, call_back_context)
        reg = re.findall('^(\d+)$', ans, re.MULTILINE)
        self.assertTrue(len(reg) == before)

    def test_close_event(self):
        create_event(update, call_back_context)
        close_event(update, call_back_context)
        flag = False
        try:
            active_event(update, call_back_context)
        except BaseException:
            flag = True
        self.assertTrue(flag)

    def test_open_event(self):
        create_event(update, call_back_context)
        create_event(update, call_back_context)
        open_event(update, call_back_context)
        update.message.text = '1'
        message_handler(update, call_back_context)
        ans = active_event(update, call_back_context)
        reg = re.findall('id: (\d+)', ans, re.MULTILINE)
        self.assertTrue(reg[0] == '1')

    def test_set_name(self):
        create_event(update, call_back_context)
        set_name(update, call_back_context)
        update.message.text = 'test_name'
        message_handler(update, call_back_context)
        ans = view_my_events(update, call_back_context)
        reg = re.findall('test_name', ans, re.MULTILINE)
        self.assertTrue(reg[0] == 'test_name')

    def test_set_description(self):
        create_event(update, call_back_context)
        set_description(update, call_back_context)
        update.message.text = 'test_description'
        message_handler(update, call_back_context)
        ans = view_my_events(update, call_back_context)
        reg = re.findall('test_description', ans, re.MULTILINE)
        self.assertTrue(reg[0] == 'test_description')

    def test_set_datetime(self):
        create_event(update, call_back_context)
        set_datetime(update, call_back_context)
        update.message.text = '04-06-2021-04-42'
        message_handler(update, call_back_context)
        ans = view_my_events(update, call_back_context)
        reg = re.findall('04-06-2021-04-42', ans, re.MULTILINE)
        self.assertTrue(reg[0] == '04-06-2021-04-42')

    def test_add_subscribers(self):
        create_event(update, call_back_context)
        add_subscribers(update, call_back_context)
        update.message.text = '1111111'
        message_handler(update, call_back_context)
        ans = view_my_events(update, call_back_context)
        print(ans)
        reg = re.findall('1111111', ans, re.MULTILINE)
        self.assertTrue(reg[0] == '1111111')

    def test_delete_subscribers(self):
        ans = view_my_events(update, call_back_context)
        reg = re.findall('1111111', ans, re.MULTILINE)
        before = len(reg)
        create_event(update, call_back_context)
        add_subscribers(update, call_back_context)
        update.message.text = '1111111'
        message_handler(update, call_back_context)
        delete_subscribers(update, call_back_context)
        message_handler(update, call_back_context)
        ans = view_my_events(update, call_back_context)
        print(ans)
        reg = re.findall('1111111', ans, re.MULTILINE)
        self.assertTrue(len(reg) == before)

    def test_my_id(self):
        ans = my_id(update, call_back_context)
        reg = re.findall('1', ans, re.MULTILINE)
        self.assertTrue(reg[0] == '1')

    def test_view_my_notifications(self):
        create_event(update, call_back_context)
        ans = view_my_notifications(update, call_back_context)
        reg = re.findall('1', ans, re.MULTILINE)
        self.assertTrue(reg[0] == '1')

    def test_set_datetime_notification_by_id(self):
        create_event(update, call_back_context)
        set_datetime_notification_by_id(update, call_back_context)
        update.message.text = '1 04-06-2021-04-42'
        message_handler(update, call_back_context)
        ans = view_my_notifications(update, call_back_context)
        reg = re.findall('04-06-2021-04-42', ans, re.MULTILINE)
        self.assertTrue(reg[0] == '04-06-2021-04-42')

    def test_set_title_notification_by_id(self):
        create_event(update, call_back_context)
        set_title_notification_by_id(update, call_back_context)
        update.message.text = '1 test_title'
        message_handler(update, call_back_context)
        ans = view_my_notifications(update, call_back_context)
        reg = re.findall('test_title', ans, re.MULTILINE)
        self.assertTrue(reg[0] == 'test_title')