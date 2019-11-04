from django.contrib import admin
from webapp.models import Task, Status, Type, Project, Team


class TaskAdmin(admin.ModelAdmin):
    list_display = ['pk', 'summary', 'description', 'project', 'status', 'type', 'created_at', 'updated_at']
    list_filter = ['project', 'status', 'type']
    list_display_links = ['pk', 'summary', 'description']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'created_at', 'updated_at', 'project_status']
    list_filter = ['name', 'created_at', 'project_status']
    list_display_links = ['name']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'project']
    list_filter = ['user', 'project']


admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Team, TeamAdmin)

