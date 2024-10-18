# accounts/middleware.py
from django.utils.timezone import now
from .models import APICallLog
import re

class APICallTrackingMiddleware:
    """
    Middleware to log API calls along with the user's identity, platform (web or mobile),
    and other relevant details.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/api/'):  # Adjust this based on your API path
            self.log_api_call(request)

        return response

    def log_api_call(self, request):
        user = request.user if request.user.is_authenticated else None
        platform = self.get_platform(request)
        
        APICallLog.objects.create(
            user=user,
            method=request.method,
            endpoint=request.path,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            platform=platform
        )

    def get_client_ip(self, request):
        """Extracts client IP from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_platform(self, request):
        """Determine whether the request is from a mobile or web client."""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if re.search('mobile|android|iphone|ipad', user_agent):
            return 'mobile'
        return 'web'
