from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('preferences/', views.NotificationPreferenceUpdateView.as_view(), name='preference-update'),
    path('history/', views.NotificationHistoryView.as_view(), name='history'),
    path('<int:notification_id>/', views.NotificationDetailView.as_view(), name='detail'),
]
