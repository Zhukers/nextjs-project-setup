from django import forms
from .models import Sticker

class StickerForm(forms.ModelForm):
    class Meta:
        model = Sticker
        fields = ['title', 'description', 'image', 'category', 'city', 'price', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white focus:outline-none focus:border-blue-500',
                'placeholder': 'Введите название стикера'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white focus:outline-none focus:border-blue-500',
                'placeholder': 'Опишите ваш стикер',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white focus:outline-none focus:border-blue-500',
                'placeholder': '0.00'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white focus:outline-none focus:border-blue-500'
            }),
            'city': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-700 rounded-lg bg-gray-800 text-white focus:outline-none focus:border-blue-500'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 rounded border-gray-700 bg-gray-800 focus:ring-blue-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'hidden',
            'id': 'image-upload'
        })
        # Add custom file input styling
        self.fields['image'].widget.template_name = 'stickers/widgets/image_input.html'
