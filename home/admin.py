from django.contrib import admin
from .models import Record

class RecordAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Record,RecordAdmin)
