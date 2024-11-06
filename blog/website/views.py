from django.views.generic import TemplateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, CreateView
from .models import BlogItems, BlogComment
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import PostForm
from .mixins import PaginatedViewMixin
from django.shortcuts import render, redirect, get_object_or_404


class AllItemsView(PaginatedViewMixin, LoginRequiredMixin, TemplateView):
    template_name = "website/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "COMPUTER SCIENCE"
        context["posts"] = BlogItems.objects.all()
        items = BlogItems.objects.all()  # Fetch all blog items
        context["page_obj"] = self.paginate_queryset(items, self.paginate_by)
        return context


class BlogPostDetailView(PaginatedViewMixin, DetailView):
    model = BlogItems
    template_name = "website/single_post.html"

    def get(self, request, pk):
        post = get_object_or_404(BlogItems, pk=pk)
        comments = BlogComment.objects.filter(blogpost_connected=post).order_by(
            "-date_posted"
        )
        user_liked = (
            request.user in post.liked_by.all()
        )  # Check if the user has liked the post
        user_disliked = (
            request.user in post.disliked_by.all()
        )  # Check if the user has disliked the post

        paginated_comments = self.paginate_queryset(comments, self.paginate_by)

        return render(
            request,
            "website/single_post.html",
            {
                "post": post,
                "comments": paginated_comments,
                "user_liked": user_liked,
                "user_disliked": user_disliked,
            },
        )

    def post(self, request, pk):
        post = get_object_or_404(BlogItems, pk=pk)
        if "content" in request.POST:
            new_comment = BlogComment(
                content=request.POST.get("content"),
                author=request.user,
                blogpost_connected=post,
            )
            new_comment.save()
            return redirect("website:detail", pk=pk)

        # Handle likes
        if request.POST.get("action") == "like":
            if request.user in post.liked_by.all():
                post.likes -= 1
                post.liked_by.remove(request.user)
            else:
                # Remove dislike if exists
                if request.user in post.disliked_by.all():
                    post.dislikes -= 1
                    post.disliked_by.remove(request.user)

                post.likes += 1
                post.liked_by.add(request.user)
            post.save()
            return redirect("website:detail", pk=pk)

        # Handle dislikes
        if request.POST.get("action") == "dislike":
            if request.user in post.disliked_by.all():
                post.dislikes -= 1
                post.disliked_by.remove(request.user)
            else:
                # Remove like if exists
                if request.user in post.liked_by.all():
                    post.likes -= 1
                    post.liked_by.remove(request.user)

                post.dislikes += 1
                post.disliked_by.add(request.user)
            post.save()
            return redirect("website:detail", pk=pk)

        comments = BlogComment.objects.filter(blogpost_connected=post).order_by(
            "-date_posted"
        )
        return render(
            request,
            "website/single_post.html",
            {
                "post": post,
                "comments": comments,
            },
        )


class MyPostsView(PaginatedViewMixin, LoginRequiredMixin, TemplateView):
    template_name = "website/myposts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Posts"
        context["posts"] = BlogItems.objects.filter(user=self.request.user)
        context["page_obj"] = self.paginate_queryset(
            BlogItems.objects.filter(user=self.request.user), self.paginate_by
        )
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
    form_class = PostForm
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
        context["post"] = self.object  # Make the post available in the template
        context["title"] = "Update Post"
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = "website/create_post.html"
    form_class = PostForm
    success_url = reverse_lazy("website:myposts")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating post.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Post"
        return context
