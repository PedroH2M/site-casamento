from django import forms
from .models import Gift, Category

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['category', 'name', 'description', 'image', 'total_quantity', 'status']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Liquidificador 110v'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalhes do presente...'}),
            'total_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
