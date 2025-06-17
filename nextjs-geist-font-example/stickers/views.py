from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sticker
from .forms import StickerForm

from cities.models import City

def home(request):
    cities = City.objects.all()
    return render(request, 'stickers/home.html', {'cities': cities})

@login_required
def create_sticker(request):
    if request.method == 'POST':
        form = StickerForm(request.POST, request.FILES)
        if form.is_valid():
            sticker = form.save(commit=False)
            sticker.user = request.user
            sticker.save()
            messages.success(request, 'Стикер успешно создан!')
            return redirect('stickers:sticker_detail', pk=sticker.pk)
    else:
        form = StickerForm()
    return render(request, 'stickers/sticker_form.html', {'form': form, 'title': 'Создать стикер'})

def sticker_detail(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)
    return render(request, 'stickers/sticker_detail.html', {'sticker': sticker})

@login_required
def edit_sticker(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)
    if request.user != sticker.user:
        messages.error(request, 'У вас нет прав на редактирование этого стикера.')
        return redirect('stickers:sticker_detail', pk=pk)
    
    if request.method == 'POST':
        form = StickerForm(request.POST, request.FILES, instance=sticker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Стикер успешно обновлен!')
            return redirect('stickers:sticker_detail', pk=pk)
    else:
        form = StickerForm(instance=sticker)
    return render(request, 'stickers/sticker_form.html', {
        'form': form,
        'title': 'Редактировать стикер',
        'sticker': sticker
    })

@login_required
def delete_sticker(request, pk):
    sticker = get_object_or_404(Sticker, pk=pk)
    if request.user != sticker.user:
        messages.error(request, 'У вас нет прав на удаление этого стикера.')
        return redirect('stickers:sticker_detail', pk=pk)
    
    if request.method == 'POST':
        sticker.delete()
        messages.success(request, 'Стикер успешно удален!')
        return redirect('stickers:home')
    return render(request, 'stickers/sticker_confirm_delete.html', {'sticker': sticker})
