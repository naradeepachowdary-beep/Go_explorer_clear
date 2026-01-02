from django.urls import path
from . import views
from .operator_forms import register_bus_operator, operator_dashboard

app_name = 'buses'

urlpatterns = [
    # Web routes
    path('', views.bus_list, name='bus_list'),
    path('<int:bus_id>/', views.bus_detail, name='bus_detail'),
    path('<int:bus_id>/book/', views.book_bus, name='book_bus'),
    
    # Operator registration & dashboard
    path('operator/register/', register_bus_operator, name='operator_register'),
    path('operator/dashboard/', operator_dashboard, name='operator_dashboard'),
    
    # API routes
    path('search/', views.BusSearchView.as_view(), name='bus-search'),
    path('routes/', views.BusRouteListView.as_view(), name='route-list'),
    path('routes/<int:pk>/', views.BusRouteDetailView.as_view(), name='route-detail'),
]
