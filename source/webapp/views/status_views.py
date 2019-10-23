from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from webapp.models import Status
from webapp.forms import StatusForm
from django.db.models import ProtectedError


class StatusIndexView(ListView):
    context_object_name = 'statuses'
    model = Status
    template_name = 'status/status_index.html'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'status/status_create.html'
    form_class = StatusForm

    def get_success_url(self):
        return reverse('webapp:status_index')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'status/status_update.html'
    form_class = StatusForm
    context_object_name = 'status'

    def get_success_url(self):
        return reverse('webapp:status_index')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'error.html'

    def get(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, self.template_name)

    def get_success_url(self):
        return reverse('webapp:status_index')
