from django import forms
from django.contrib.auth.models import User
from .models import BusOperator, Bus, BoardingPoint, DroppingPoint


class BusOperatorRegistrationForm(forms.ModelForm):
    """Form for bus operators to register"""
    
    # User account fields
    username = forms.CharField(max_length=150, required=True, help_text="Username for login")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = BusOperator
        fields = [
            'name', 'description', 'logo', 
            'contact_phone', 'contact_email',
            'business_license', 'pan_number', 'gst_number',
            'registered_address'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'registered_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


class BusForm(forms.ModelForm):
    """Form for operators to add/edit buses"""
    
    class Meta:
        model = Bus
        exclude = ['operator', 'created_at', 'updated_at', 'average_rating', 'total_reviews']
        widgets = {
            'bus_type': forms.Select(attrs={'class': 'form-select'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'manufacturing_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1990, 'max': 2025}),
        }


class BoardingPointForm(forms.ModelForm):
    """Form for adding boarding points"""
    
    class Meta:
        model = BoardingPoint
        exclude = ['route']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sequence_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class DroppingPointForm(forms.ModelForm):
    """Form for adding dropping points"""
    
    class Meta:
        model = DroppingPoint
        exclude = ['route']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'drop_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'sequence_order': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class BusSearchForm(forms.Form):
    """Enhanced bus search form with filters"""
    
    source = forms.CharField(max_length=100, required=True)
    destination = forms.CharField(max_length=100, required=True)
    journey_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    
    # Filters
    bus_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Bus.BUS_TYPES,
        required=False
    )
    departure_time = forms.ChoiceField(
        choices=[
            ('', 'Any Time'),
            ('morning', '6 AM - 12 PM'),
            ('afternoon', '12 PM - 6 PM'),
            ('evening', '6 PM - 12 AM'),
            ('night', '12 AM - 6 AM'),
        ],
        required=False
    )
    ac_only = forms.BooleanField(required=False, label="AC Buses Only")
    wifi_only = forms.BooleanField(required=False, label="WiFi Available")
    min_rating = forms.DecimalField(
        required=False, 
        min_value=0, 
        max_value=5,
        label="Minimum Rating"
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('departure', 'Departure Time'),
            ('price_low', 'Price: Low to High'),
            ('price_high', 'Price: High to Low'),
            ('rating', 'Highest Rating'),
            ('seats', 'Seats Available'),
        ],
        required=False
    )
