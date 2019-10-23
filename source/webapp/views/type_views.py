from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from webapp.models import Type
from webapp.forms import TypeForm


class TypeIndexView(ListView):
    context_object_name = 'types'
    model = Type
    template_name = 'type/type_index.html'


class TypeCreateView(LoginRequiredMixin, CreateView):
    model = Type
    template_name = 'type/type_create.html'
    form_class = TypeForm

    def get_success_url(self):
        return reverse('webapp:type_index')


class TypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Type
    template_name = 'type/type_update.html'
    form_class = TypeForm
    context_object_name = 'type'

    def get_success_url(self):
        return reverse('webapp:type_index')


class TypeDeleteView(LoginRequiredMixin, DeleteView):
    model = Type
    template_name = 'error.html'

    def get(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, self.template_name)

    def get_success_url(self):
        return reverse('webapp:type_index')
