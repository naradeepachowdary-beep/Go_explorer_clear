from django.urls import path
from . import views

app_name = 'property_owners'

urlpatterns = [
    path('register/', views.register_property_owner, name='register'),
    path('dashboard/', views.property_owner_dashboard, name='dashboard'),
    path('add-property/', views.add_property, name='add_property'),
]
