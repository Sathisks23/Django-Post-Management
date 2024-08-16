from django import forms
from .models import Category
from .models import Category,Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'img_url']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'img_url': forms.FileInput(attrs={'class': 'form-control'}),
        }
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']