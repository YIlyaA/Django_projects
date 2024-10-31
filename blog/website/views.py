from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BlogItems

class AllItemsView(LoginRequiredMixin, TemplateView):
    template_name = 'website/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = BlogItems.objects.all()    
        return context
