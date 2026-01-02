from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
