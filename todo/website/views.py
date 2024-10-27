import json
from typing import Any, Dict
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from website.models import ToDoItems
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect, JsonResponse
from website.forms import ToDoItemForm
from django.urls import reverse_lazy


class ItemsView(LoginRequiredMixin, ListView, FormMixin):
    template_name = "website/index.html"
    success_url = reverse_lazy('website:index')
    form_class = ToDoItemForm
    
    def get_queryset(self):
        return ToDoItems.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Ensure 'object_list' is defined for the ListView
        if not hasattr(self, 'object_list'):
            self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_queryset()
        context['form'] = ToDoItemForm()
        return context
    
    def post(self, request, *args, **kwargs):
        # Get the form without validation
        form = self.get_form()
        # Save the item directly, assuming client validation
        item = form.save(commit=False)
        item.user = self.request.user
        item.save()
        return HttpResponseRedirect(self.success_url)


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = ToDoItems
    success_url = reverse_lazy('website:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


class UpdateItem(LoginRequiredMixin, UpdateView):
    model = ToDoItems
    fields = ['description']

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':   #save item with ajax
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return JsonResponse({'error': 'Non-AJAX request received'}, status=400)
    

class UpdateStatus(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Parse JSON data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        # Check if the request is specifically for a status update
        item = get_object_or_404(ToDoItems, pk=kwargs['pk'], user=request.user)
        status = data.get('status')
        
        # Ensure status is provided
        if status is None:
            return JsonResponse({'error': 'Missing status field'}, status=400)

        # Update the item's status and save
        item.status = status
        item.save()

        return JsonResponse({'success': True, 'status': item.status})
