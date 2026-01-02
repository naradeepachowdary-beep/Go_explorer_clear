from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking-list'),
    path('<uuid:booking_id>/', views.BookingDetailView.as_view(), name='booking-detail'),
]
