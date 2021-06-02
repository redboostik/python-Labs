from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'name')
    form = UserForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'date', 'owner_ID', 'subscribers')
    form = EventForm


@admin.register(ActiveEvents)
class ActiveEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_ID', 'event_ID')
    form = ActiveEventsForm


@admin.register(ActiveCommand)
class ActiveEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_ID', 'command')
    form = ActiveCommandForm
