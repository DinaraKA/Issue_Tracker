from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from webapp.models import Task, Project, Team
from webapp.forms import TaskForm, ProjectTaskForm, SimpleSearchForm


class IndexView(ListView):
    context_object_name = 'tasks'
    model = Task
    template_name = 'task/index.html'
    ordering = ['-created_at']
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_query = self.get_search_query()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.search_query:
            context['query'] = urlencode({'search': self.search_query})
        context['form'] = self.form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_query:
            queryset = queryset.filter(
                Q(summary__icontains=self.search_query)
                | Q(description__icontains=self.search_query)
            ).distinct()
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_query(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class TaskView(DetailView):
    context_object_name = 'task'
    model = Task
    pk_url_kwarg = 'pk'
    template_name = 'task/task.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task/create.html'
    form_class = TaskForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form()
        user_projects_list = Team.objects.filter(user__username=self.request.user).values_list('project', flat=None)
        form.fields['project'].queryset = Project.objects.filter(pk__in=user_projects_list)
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        users_list = Team.objects.filter(user__username=self.request.user).values_list('user', flat=None)
        kwargs['users_list'] = users_list
        return kwargs


class TaskProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'task/create.html'
    form_class = ProjectTaskForm

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        project.tasks.create(**form.cleaned_data)
        return redirect('webapp:project_view', pk=project_pk)


class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task/update.html'
    form_class = TaskForm
    context_object_name = 'task'

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        users_list = Team.objects.filter(user__username=self.request.user).values_list('user', flat=None)
        kwargs['users_list'] = users_list
        return kwargs


    def test_func(self, **kwargs):
        task = Task.objects.get(pk=self.kwargs.get('pk'))
        project = Project.objects.get(pk=task.project.pk)
        user_pk_list = Team.objects.filter(project=project, end=None).distinct().values_list('user_id', flat=True)
        if self.request.user.pk in user_pk_list:
            return True
        else:
            return False


class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'task/delete.html'
    success_url = reverse_lazy('webapp:index')


    def test_func(self, **kwargs):
        task = Task.objects.get(pk=self.kwargs.get('pk'))
        project = Project.objects.get(pk=task.project.pk)
        team = Team.objects.filter(project=project, end=None).distinct()
        user_pk_list = team.values_list('user_id', flat=True)
        if self.request.user.pk in user_pk_list:
            return True
        else:
            return False

