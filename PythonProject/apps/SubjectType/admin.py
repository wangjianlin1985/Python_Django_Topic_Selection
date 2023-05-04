from django.contrib import admin
from apps.SubjectType.models import SubjectType

# Register your models here.

admin.site.register(SubjectType,admin.ModelAdmin)