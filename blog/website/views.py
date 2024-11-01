from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from .models import BlogItems
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PostUpdateForm


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


class UpdatePostView(LoginRequiredMixin, UpdateView):
    template_name = "website/update_post.html"
    form_class = PostUpdateForm
    model = BlogItems

    def get_success_url(self):
        return reverse_lazy("website:myposts")

    def form_valid(self, form):
        messages.success(self.request, "Successfully updated.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating post.")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object  # Make the post available in the template
        context['title'] = 'Update Post'
        return context
