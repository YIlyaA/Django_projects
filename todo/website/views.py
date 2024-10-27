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