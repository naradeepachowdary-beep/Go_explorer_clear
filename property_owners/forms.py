from django import forms
from .models import PropertyOwner, Property
from core.models import City


class PropertyOwnerRegistrationForm(forms.ModelForm):
    """Registration form for property owners"""
    city = forms.ModelChoiceField(queryset=City.objects.all().order_by('name'), label='City/Location')
    
    class Meta:
        model = PropertyOwner
        fields = [
            'business_name', 'property_type', 'description', 'owner_name',
            'owner_phone', 'owner_email', 'city', 'address', 'pincode',
            'gst_number', 'pan_number', 'bank_account_name',
            'bank_account_number', 'bank_ifsc'
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your property business name'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your property...'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'owner_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'owner_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full property address'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '560001'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: XX XXXXX XXXX X XXX'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: XXXXX XXXXX XXXXX'}),
            'bank_account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account holder name'}),
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account number'}),
            'bank_ifsc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IFSC code'}),
        }


class PropertyForm(forms.ModelForm):
    """Form for creating/editing properties"""
    class Meta:
        model = Property
        fields = ['name', 'description', 'amenities', 'base_price', 'max_guests', 'num_bedrooms', 'num_bathrooms', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'WiFi, Pool, Kitchen, AC...'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_guests': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
