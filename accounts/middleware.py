from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import time

class LogoutProtectionMiddleware:
    """
    Middleware to prevent accidental logout via browser navigation.
    This intercepts ALL requests to logout URLs and validates them.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # NO LOGOUT URLS EXIST ANYMORE - this middleware is now for other protection
        # All logout functionality has been moved to session-destroy endpoint
        
        response = self.get_response(request)
        return response

    def handle_logout_request(self, request):
        """Handle all logout requests with COMPLETE BLOCKING"""
        
        # Log all logout attempts for debugging
        print(f"MIDDLEWARE BLOCKED LOGOUT: Method={request.method}, Path={request.path}, User={request.user.username if request.user.is_authenticated else 'Anonymous'}")
        
        # NEVER allow logout via original URL - always redirect
        return self.redirect_to_dashboard(request, "Logout blocked by security middleware. Use the dashboard logout button.")
    
    def redirect_to_dashboard(self, request, message):
        """Redirect user back to appropriate dashboard with message"""
        messages.warning(request, message)
        
        if request.user.is_authenticated:
            try:
                from accounts.models import UserProfile
                profile = UserProfile.objects.get(user=request.user, user_type='organizer')
                return redirect('organizer-dashboard')
            except UserProfile.DoesNotExist:
                try:
                    profile = UserProfile.objects.get(user=request.user, user_type='student')
                    return redirect('student-dashboard')
                except UserProfile.DoesNotExist:
                    return redirect('organizer-dashboard')
        
        return redirect('landing')