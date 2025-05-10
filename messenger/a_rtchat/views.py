from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroup
from .forms import ChatMessageCreateForm


@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.group = chat_group
            message.author = request.user
            message.save()
            context = {
                "message": message,
                "user": request.user,
            }
            return render(request, "a_rtchat/partials/chat_message_p.html", context)
    return render(
        request, "a_rtchat/chat.html", {"chat_messages": chat_messages, "form": form}
    )
