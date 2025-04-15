from django import forms
from .models import Recipe, Profile, Ingredient, RecipeIngredient
from django.forms import inlineformset_factory

class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control select2-ingredient',
            'data-placeholder': 'Select an ingredient'
        }),
        required=True
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'notes']
        widgets = {
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1 cup'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. finely chopped'
            }),
        }

# Formset factory for ingredients
RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
    fields=['ingredient', 'quantity', 'notes']
)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'instructions', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the recipe'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Step-by-step instructions'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website', 'location']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself...'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your location'
            }),
        }