
from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(AdminRequest)
class AdminRequestAdmin(admin.ModelAdmin):
    list_display = ('user','approved','requested_at')
    list_editable = ('approved',)