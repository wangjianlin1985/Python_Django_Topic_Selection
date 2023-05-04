from django.contrib import admin
from apps.Subject.models import Subject

# Register your models here.

admin.site.register(Subject,admin.ModelAdmin)