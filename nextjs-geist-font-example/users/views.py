from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from users.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import Http404

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate user to get backend info
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('stickers:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("User does not exist")
    else:
        user = request.user
    return render(request, 'users/profile.html', {'profile_user': user})
