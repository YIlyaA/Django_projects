from multiprocessing import context
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from .models import BlogItems
from django.urls import reverse_lazy
from django.contrib import messages


class AllItemsView(LoginRequiredMixin, TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COMPUTER SCIENCE"
        context["posts"] = BlogItems.objects.all()
        return context


class MyPostsView(LoginRequiredMixin, TemplateView):
    template_name = "website/myposts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Posts"
        context["posts"] = BlogItems.objects.filter(user=self.request.user)
        return context


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = BlogItems
    success_url = reverse_lazy("website:myposts")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()  # Retrieve the object to be deleted
        self.object.delete()  # Delete the object manually (custom handling can be added here)
        messages.success(
            self.request, "Successfully deleted."
        )  # Custom message after deletion
