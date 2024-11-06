from django.db import models
from django.utils import timezone


class BlogItems(models.Model):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField("users.CustomUser", related_name='liked_posts', blank=True)
    disliked_by = models.ManyToManyField("users.CustomUser", related_name='disliked_posts', blank=True)

    def __str__(self):
        return self.title

    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(blogpost_connected=self).count()


class BlogComment(models.Model):
    blogpost_connected = models.ForeignKey(
        BlogItems, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ", " + self.blogpost_connected.title[:40]
