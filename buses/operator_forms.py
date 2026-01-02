from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from buses.models import BusOperator
from django import forms


class BusOperatorRegistrationForm(forms.ModelForm):
    """Registration form for bus operators"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
    
    class Meta:
        model = BusOperator
        fields = ['name', 'description', 'contact_phone', 'contact_email', 'gst_number', 'pan_number', 'business_license', 'registered_address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bus company name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'About your bus service...'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXXXXXXX'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@buscompany.com'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '27AABCU9603R1Z0'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXX XXXXX XXXXX'}),
            'business_license': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License number'}),
            'registered_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Registered office address'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')
        
        return cleaned_data


def register_bus_operator(request):
    """Register as a bus operator"""
    from django.contrib.auth import authenticate, login
    from users.models import User
    
    if request.method == 'POST':
        form = BusOperatorRegistrationForm(request.POST)
        if form.is_valid():
            # Create user account
            email = form.cleaned_data.get('contact_email')
            password = form.cleaned_data.get('password')
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'buses/operator_register.html', {'form': form})
            
            # Create user
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password=password,
                first_name=form.cleaned_data.get('name', '').split()[0] if form.cleaned_data.get('name') else '',
            )
            
            # Create operator profile
            operator = form.save(commit=False)
            operator.user = user
            operator.save()
            
            # Auto-login
            login(request, user)
            messages.success(request, 'Registration successful! Your account is pending verification by our team.')
            return redirect('buses:operator_dashboard')
    else:
        form = BusOperatorRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register as Bus Operator',
    }
    return render(request, 'buses/operator_register.html', context)


@login_required
def operator_dashboard(request):
    """Dashboard for bus operators"""
    try:
        operator = request.user.bus_operator_profile
    except BusOperator.DoesNotExist:
        messages.warning(request, "Please register as a bus operator first.")
        return redirect('buses:operator_register')
    
    buses = operator.buses.all()
    routes = sum(b.routes.count() for b in buses)
    
    context = {
        'operator': operator,
        'buses': buses,
        'stats': {
            'total_buses': buses.count(),
            'total_routes': routes,
            'verification_status': operator.get_verification_status_display(),
        }
    }
    return render(request, 'buses/operator_dashboard.html', context)
