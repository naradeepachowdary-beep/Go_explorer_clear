from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    # Web pages (for /hotels/ path)
    path('', views.hotel_list, name='hotel_list'),
    path('<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('<int:pk>/book/', views.book_hotel, name='book_hotel'),
    
    # API endpoints (also available under /api/hotels/)
    path('list/', views.HotelListView.as_view(), name='hotel-list'),
    path('search/', views.HotelSearchView.as_view(), name='hotel-search'),
    path('<int:pk>/api/', views.HotelDetailView.as_view(), name='hotel-detail-api'),
]
