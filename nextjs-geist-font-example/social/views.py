from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import UserFollow, UserMessage

User = get_user_model()

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    if user_to_follow == request.user:
        messages.error(request, 'Вы не можете подписаться на самого себя.')
        return redirect('users:profile', username=user_to_follow.username)
    
    follow, created = UserFollow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if created:
        messages.success(request, f'Вы подписались на {user_to_follow.username}')
    else:
        messages.info(request, f'Вы уже подписаны на {user_to_follow.username}')
    
    return redirect('users:profile', username=user_to_follow.username)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    try:
        follow = UserFollow.objects.get(
            follower=request.user,
            following=user_to_unfollow
        )
        follow.delete()
        messages.success(request, f'Вы отписались от {user_to_unfollow.username}')
    except UserFollow.DoesNotExist:
        messages.error(request, f'Вы не были подписаны на {user_to_unfollow.username}')
    
    return redirect('users:profile', username=user_to_unfollow.username)

@login_required
def followers_list(request):
    followers = UserFollow.objects.filter(following=request.user).select_related('follower')
    return render(request, 'social/followers_list.html', {'followers': followers})

@login_required
def following_list(request):
    following = UserFollow.objects.filter(follower=request.user).select_related('following')
    return render(request, 'social/following_list.html', {'following': following})

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            UserMessage.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )
            messages.success(request, 'Сообщение отправлено')
            return redirect('social:messages')
        else:
            messages.error(request, 'Сообщение не может быть пустым')
    
    return render(request, 'social/send_message.html', {'recipient': recipient})

@login_required
def messages_list(request):
    received_messages = UserMessage.objects.filter(recipient=request.user).select_related('sender')
    sent_messages = UserMessage.objects.filter(sender=request.user).select_related('recipient')
    
    # Mark received messages as read
    received_messages.filter(is_read=False).update(is_read=True)
    
    return render(request, 'social/messages_list.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })
