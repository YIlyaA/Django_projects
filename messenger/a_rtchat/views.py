from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import ChatGroup
from .forms import ChatMessageCreateForm, NewGroupForm, ChatRoomEditForm
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def chat_view(request, chatroom_name="public-chat"):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.membres.all():
            raise Http404()
        for memeber in chat_group.membres.all():
            if memeber != request.user:
                other_user = memeber
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.membres.all():
            if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.membres.add(request.user)
            else:
                messages.warning(
                    request, "Please verify your email address to join this chat."
                )
                return redirect("profile-settings")

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

    context = {
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
        "chat_group": chat_group,
    }
    return render(request, "a_rtchat/chat.html", context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect("home")

    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.membres.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.membres.add(other_user, request.user)

    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.membres.add(other_user, request.user)

    return redirect("chatroom", chatroom.group_name)


@login_required
def create_groupchat(request):
    form = NewGroupForm
    if request.method == "POST":
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.membres.add(request.user)
            return redirect("chatroom", new_groupchat.group_name)

    context = {
        "form": form,
    }
    return render(request, "a_rtchat/create_groupchat.html", context)


@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()

    if request.method == "POST":
        chat_group.delete()
        messages.success(request, "Chatroom deleted")
        return redirect("home")

    return render(request, "a_rtchat/chatroom_delete.html", {"chat_group": chat_group})


@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()

    form = ChatRoomEditForm(instance=chat_group)  # populating data in the form

    if request.method == "POST":
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()

            remove_members = request.POST.getlist("remove_members")
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.membres.remove(member)

            return redirect("chatroom", chatroom_name)

    context = {
        "form": form,
        "chat_group": chat_group,
    }

    return render(request, "a_rtchat/chatroom_edit.html", context)


@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user not in chat_group.membres.all():
        raise Http404()

    if request.method == "POST":
        chat_group.membres.remove(request.user)
        messages.success(request, "You left the Chat")
        return redirect("home")

    return render(request, "a_rtchat/chatroom_leave.html", {"chat_group": chat_group})
