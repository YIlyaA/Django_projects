from django.db import models
from django.db.models import CASCADE
from django.contrib.auth import get_user_model


User = get_user_model()

class ToDoItems(models.Model):
    user = models.ForeignKey(to=User, on_delete=CASCADE)
    description = models.CharField(max_length=100, blank=False, null=False)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description