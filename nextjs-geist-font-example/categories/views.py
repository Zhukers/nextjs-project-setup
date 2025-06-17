from django.shortcuts import render, get_object_or_404
from .models import Category

from django.shortcuts import render, get_object_or_404
from .models import Category
from cities.models import City

def category_list(request, city_id=None):
    if city_id:
        city = get_object_or_404(City, pk=city_id)
        categories = Category.objects.filter(city=city)
    else:
        categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories, 'city': city if city_id else None})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    stickers = category.sticker_set.all()
    return render(request, 'categories/category_detail.html', {
        'category': category,
        'stickers': stickers
    })
