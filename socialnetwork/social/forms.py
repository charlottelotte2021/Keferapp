from unittest.util import _MAX_LENGTH
from django import forms
from .models import Post, ThreadModel, MessageModel

class PostForm(forms.ModelForm): 
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder': 'Kéfir, Kombucha, Compost, Levain...',
        })
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
            })
    )

    address = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '1',
            'placeholder': 'Où se trouve votre produit ?'
        })
    )

    category = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '1',
            'placeholder': 'Quelle est la catégorie de votre produit'
        })
    )

    class Meta: 
        model = Post 
        fields = [
            'body',
            'image',
            'address'
        ]


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000)
    image = forms.ImageField(required=False)
    class Meta: 
        model= MessageModel 
        fields = ['body', 'image']

class ExploreForm(forms.Form):
    query = forms.CharField(
        label = '',
        widget = forms.TextInput(attrs={
            'placeholder':'Cherchez des produits'
        }),
    )

# class SearchAddress(forms.ModelForm):
#     body = forms.CharField(label='', max_length=1000)
#     class Meta: 
#         model = Address
#         fields = ['body']
