from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ProjectTaskForm, ProjectForm, SimpleSearchForm, ProjectUserForm
from webapp.models import Project, Team
from webapp.views.base_views import SessionStatMixin


class ProjectIndexView(SessionStatMixin, ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'project/project_index.html'
    ordering = ['created_at']
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
                Q(name__icontains=self.search_query)
            )
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_query(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectView(SessionStatMixin, DetailView):
    context_object_name = 'project'
    model = Project
    pk_url_kwarg = 'pk'
    template_name = 'project/project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = context['project'].tasks.order_by('-created_at')
        context['team_users']= Team.objects.filter(project=self.object, end=None)
        self.paginate_tasks_to_context(projects, context)
        return context

    def paginate_tasks_to_context(self, tasks, context):
        paginator = Paginator(tasks, 3, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['tasks'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class ProjectCreateView(PermissionRequiredMixin, SessionStatMixin, CreateView):
    model = Project
    template_name = 'project/project-create.html'
    form_class = ProjectForm
    permission_required = 'webapp.add_project', 'webapp.add_team'
    permission_denied_message = 'Access is denied!'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_index')

    def form_valid(self, form):
        users_list = list(form.cleaned_data.pop('users'))
        users_list.append(self.request.user)
        self.object = form.save()
        for user in users_list:
            Team.objects.create(user=user, project=self.object, start=datetime.now())
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(PermissionRequiredMixin, SessionStatMixin, UpdateView):
    model = Project
    template_name = 'project/project_update.html'
    fields = ['name', 'description']
    context_object_name = 'project'
    permission_required = 'webapp.change_project'
    permission_denied_message = 'Access is denied!'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectUsersUpdate(PermissionRequiredMixin, SessionStatMixin, UpdateView):
    model = Project
    form_class = ProjectUserForm
    template_name = 'project/project-user_edit.html'
    permission_required = 'webapp.add_team', 'webapp.change_team'
    permission_denied_message = 'Access is denied!'

    def get_initial(self):
        initial = super().get_initial()
        initial['users'] = User.objects.filter(user_team__project=self.object, user_team__end=None)
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_users']= Team.objects.filter(project=self.object, end=None)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        project_pk = self.kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_pk)
        users_list = list(form.cleaned_data.pop('users'))
        self.object = form.save()
        project_users = Team.objects.filter(project=project, end=None)
        for user in users_list:
            if user not in project_users:
                Team.objects.create(user=user, project=project, start=datetime.now())
        for user in project_users:
            if user not in users_list:
                user.end = datetime.now()
                user.save()
        return redirect('webapp:project_view', pk=project_pk)


class ProjectDeleteView(PermissionRequiredMixin, SessionStatMixin, DeleteView):
    model = Project
    template_name = 'error.html'
    permission_required = 'webapp.delete_project'
    permission_denied_message = 'Access is denied!'

    def get(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, self.template_name)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_index')




