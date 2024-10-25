import json
from typing import Any, Dict
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from website.models import ToDoItems
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from website.forms import ToDoItemForm
from django.urls import reverse_lazy


class ItemsView(LoginRequiredMixin, ListView):
    template_name = "website/index.html"
    success_url = reverse_lazy('website:index')
    
    
    def get_queryset(self):
        return ToDoItems.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        context['form'] = ToDoItemForm()
        return context
    

    def post(self, request, *args, **kwargs):
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = self.request.user
            item.save()

            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)
        

    def form_invalid(self, form):
        # Handle form errors (for non-AJAX requests)
        return JsonResponse({'errors': form.errors}, status=400)


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = ToDoItems
    success_url = reverse_lazy('website:index')


class UpdateItem(LoginRequiredMixin, UpdateView):
    model = ToDoItems
    success_url = reverse_lazy('website:index')

    def post(self, request, *args, **kwargs):
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = self.request.user
            item.save()

            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)
