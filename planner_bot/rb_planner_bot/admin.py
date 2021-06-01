from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'name')
    form = UserForm


@admin.register(Event)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner_ID', 'subscribers')
    form = EventForm
