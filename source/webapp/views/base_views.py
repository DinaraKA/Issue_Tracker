from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime


class ListView(TemplateView):
    context_key = 'objects'
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_key] = self.get_oblects()
        return context

    def get_oblects(self):
        return self.model.objects.all()


class DetailView(TemplateView):
    context_key = 'object'
    model = None
    key_kwargs = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_key] = get_object_or_404(self.model, pk=self.kwargs.get(self.key_kwargs))
        return context


class CreateView(View):
    form_class = None
    template_name = None
    model = None
    redirect_url = ''

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, context={'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_redirect_url(self):
        return self.redirect_url

    def form_valid(self, form):
        self.object = self.model.objects.create(**form.cleaned_data)
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        return render(self.request, self.template_name, context={'form':form})


class UpdateView(View):
    form_class = None
    template_name = None
    model = None
    redirect_url = ''
    key_kwarg = 'pk'
    context_key = 'object'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(initial=self.get_form_initial())
        context = self.make_context(form)
        return render(request, self.template_name, context=context)

    def get_form_initial(self):
        model_fields = [field.name for field in self.model._meta.fields]
        initial = {}
        for field in model_fields:
            initial[field] = getattr(self.object, field)
        print(initial)
        return initial

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()
        for field, value in form.cleaned_data.items():
            setattr(self.object, field, value)
        self.object.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = self.make_context(form)
        return render(self.request, self.template_name, context=context)

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)

    def make_context(self, form):
        return {
            'form': form,
            self.context_key: self.object
        }

    def get_redirect_url(self):
        return self.redirect_url


class DeleteView(View):
    template_name = None
    confirm_deletion = True
    model = None
    key_kwarg = 'pk'
    context_key = 'object'
    redirect_url = ''

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.confirm_deletion:
            return render(request, self.template_name, self.get_context_data())
        else:
            self.perform_delete()
            return redirect(self.get_redirect_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.perform_delete()
        return redirect(self.get_redirect_url())

    def perform_delete(self):
        self.object.delete()

    def get_context_data(self, **kwargs):
        return {self.context_key: self.object}

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)

    def get_redirect_url(self):
        return self.redirect_url


class SessionStatMixin(View):
    def get(self, request, *args, **kwargs):
        self.page_visits_count()
        self.visits_total()
        last_page = request.session.get('last_page')
        now = datetime.now()
        if last_page:
            diff = self.get_time_spent(now)
            self.update_page_times(diff, last_page)
            self.update_times_total(diff)
        self.update_last_page_info(now)
        return super().get(request, *args, **kwargs)

    def page_visits_count(self):
        visits = self.request.session.get('page_visits', {})
        current_page_visits = visits.get(self.request.path, 0)
        current_page_visits += 1
        visits[self.request.path] = current_page_visits
        self.request.session['page_visits'] = visits

    def visits_total(self):
        total_visits = self.request.session.get('visits_total', 0)
        total_visits += 1
        self.request.session['visits_total'] = total_visits

    def get_time_spent(self, now):
        last_time = self.request.session.get('last_time')
        last_time = datetime.strptime(last_time, '%Y-%m-%d %H:%M:%S')
        return (now - last_time).total_seconds()

    def update_page_times(self, diff, last_page):
        times = self.request.session.get('page_times', {})
        last_page_time = times.get(last_page, 0)
        last_page_time += diff
        times[last_page] = last_page_time
        self.request.session['page_times'] = times

    def update_times_total(self, diff):
        total_time = self.request.session.get('times_total', 0)
        total_time += diff
        self.request.session['times_total'] = total_time

    def update_last_page_info(self, now):
        self.request.session['last_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
        self.request.session['last_page'] = self.request.path




