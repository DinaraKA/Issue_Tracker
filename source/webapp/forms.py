from django import forms
from django.forms import widgets
from webapp.models import Status, Type, Task, Project


# class TaskForm(forms.Form):
#     summary = forms.CharField(max_length=100, required=True, label='Summary')
#     description = forms.CharField(max_length=2000, required=False, label='Description',
#                            widget=widgets.Textarea)
#     status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Status', empty_label=None)
#     type = forms.ModelChoiceField(queryset=Type.objects.all(), label="Type", empty_label=None)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'project', 'status', 'type']
        object = 'task'
        widgets = {
            'description': widgets.Textarea
        }



# class StatusForm(forms.Form):
#     status_name = forms.CharField(max_length=20, required=True, label='Status name')

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields =['status_name']

# class TypeForm(forms.Form):
#     type_name = forms.CharField(max_length=20, required=True, label='Type name')

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields =['type_name']


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields =['name', 'description']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")

