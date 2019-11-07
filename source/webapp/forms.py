from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from webapp.models import Status, Type, Task, Project


class TaskForm(forms.ModelForm):
    def __init__(self, users_list, **kwargs):
        super().__init__(**kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(pk__in=users_list)

    class Meta:
        model = Task
        fields = ['summary', 'description', 'project', 'status', 'type', 'assigned_to']
        object = 'task'
        widgets = {
            'description': widgets.Textarea
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields =['status_name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields =['type_name']


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type', 'assigned_to']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields =['name', 'description']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")

