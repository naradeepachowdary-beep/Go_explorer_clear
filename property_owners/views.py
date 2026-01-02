from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import PropertyOwner, Property
from .forms import PropertyOwnerRegistrationForm, PropertyForm


def register_property_owner(request):
    """Register as a property owner"""
    # Check if user already has a property owner profile
    if hasattr(request.user, 'property_owner_profile'):
        messages.info(request, "You already have a property owner account.")
        return redirect('property_owners:dashboard')
    
    if request.method == 'POST':
        form = PropertyOwnerRegistrationForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.user = request.user
            owner.save()
            messages.success(request, "Registration successful! Your account is pending verification.")
            return redirect('property_owners:dashboard')
    else:
        form = PropertyOwnerRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register as Property Owner',
    }
    return render(request, 'property_owners/register.html', context)


@login_required
def property_owner_dashboard(request):
    """Dashboard for property owners"""
    try:
        owner = request.user.property_owner_profile
    except PropertyOwner.DoesNotExist:
        messages.warning(request, "Please register as a property owner first.")
        return redirect('property_owners:register')
    
    properties = owner.properties.all()
    stats = {
        'total_properties': properties.count(),
        'total_bookings': sum(p.bookings.count() for p in properties),
        'verification_status': owner.get_verification_status_display(),
    }
    
    context = {
        'owner': owner,
        'properties': properties,
        'stats': stats,
    }
    return render(request, 'property_owners/dashboard.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def add_property(request):
    """Add new property"""
    try:
        owner = request.user.property_owner_profile
    except PropertyOwner.DoesNotExist:
        messages.error(request, "Please register as a property owner first.")
        return redirect('property_owners:register')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = owner
            property_obj.save()
            messages.success(request, "Property added successfully!")
            return redirect('property_owners:dashboard')
    else:
        form = PropertyForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Property',
    }
    return render(request, 'property_owners/add_property.html', context)
