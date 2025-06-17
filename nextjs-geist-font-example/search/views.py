from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from stickers.models import Sticker
from categories.models import Category
from cities.models import City

User = get_user_model()

def search_view(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    results = {
        'stickers': [],
        'users': [],
        'categories': [],
        'cities': []
    }
    
    if query:
        if search_type in ['all', 'stickers']:
            results['stickers'] = Sticker.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )[:10]
        
        if search_type in ['all', 'users']:
            results['users'] = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )[:10]
        
        if search_type in ['all', 'categories']:
            results['categories'] = Category.objects.filter(
                name__icontains=query
            )[:10]
        
        if search_type in ['all', 'cities']:
            results['cities'] = City.objects.filter(
                Q(name__icontains=query) |
                Q(region__icontains=query)
            )[:10]
    
    return render(request, 'search/search_results.html', {
        'query': query,
        'search_type': search_type,
        'results': results
    })

def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []
    
    if query:
        # Get sticker suggestions
        sticker_suggestions = Sticker.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True)[:5]
        suggestions.extend(list(sticker_suggestions))
        
        # Get category suggestions
        category_suggestions = Category.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:3]
        suggestions.extend(list(category_suggestions))
        
        # Get city suggestions
        city_suggestions = City.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True)[:3]
        suggestions.extend(list(city_suggestions))
    
    return JsonResponse({'suggestions': suggestions})

def advanced_search(request):
    results = []
    
    if request.GET:
        query = request.GET.get('q', '')
        category = request.GET.get('category')
        city = request.GET.get('city')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        filters = Q()
        
        if query:
            filters &= (Q(title__icontains=query) | Q(description__icontains=query))
        
        if category:
            filters &= Q(category_id=category)
        
        if city:
            filters &= Q(city_id=city)
        
        if min_price:
            filters &= Q(price__gte=min_price)
        
        if max_price:
            filters &= Q(price__lte=max_price)
        
        results = Sticker.objects.filter(filters)
    
    categories = Category.objects.all()
    cities = City.objects.all()
    
    return render(request, 'search/advanced_search.html', {
        'results': results,
        'categories': categories,
        'cities': cities
    })
