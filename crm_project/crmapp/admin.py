from django.contrib import admin
from .models import Record
from import_export.admin import ImportExportModelAdmin

class RecordAdmin(ImportExportModelAdmin):
    list_display=['created_at', 'first_name', 'last_name', 'email', 'phone', 'city', 'state']

admin.site.register(Record, RecordAdmin)