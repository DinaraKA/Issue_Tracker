from django.contrib import admin
from webapp.models import Task, Status, Type, Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ['pk', 'summary', 'description', 'project', 'status', 'type', 'created_at', 'updated_at']
    list_filter = ['project', 'status', 'type']
    list_display_links = ['pk', 'summary', 'description']

admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project)

