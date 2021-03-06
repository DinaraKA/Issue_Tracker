from django.db import models

PROJECT_STATUS = [('active', 'Active'), ('closed', 'Closed')]


class Status(models.Model):
    status_name = models.CharField(max_length=20, verbose_name='Status_name')

    def __str__(self):
        return self.status_name


class Type(models.Model):
    type_name = models.CharField(max_length=20, verbose_name='Type_name')

    def __str__(self):
        return self.type_name


class Project(models.Model):
    name = models.CharField(max_length=50, verbose_name='Project')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')
    project_status = models.CharField(max_length=20, default=PROJECT_STATUS[0][0], verbose_name='Project status', choices=PROJECT_STATUS)

    def __str__(self):
        return self.name


class Task(models.Model):
    summary = models.CharField(max_length=100, verbose_name="Summary")
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Description")
    status = models.ForeignKey(Status, related_name='tasks', on_delete=models.PROTECT, verbose_name='Status')
    type = models.ForeignKey(Type, related_name='tasks', on_delete=models.PROTECT, verbose_name='Type')
    project = models.ForeignKey(Project, null=True, related_name='tasks', on_delete=models.PROTECT,verbose_name='Project')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated date')

    def __str__(self):
        return self.summary

