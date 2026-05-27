from django.db import transaction
from .models import AuditLog


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self._log_action(request)
        return response

    def _log_action(self, request):
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            try:
                with transaction.atomic():
                    AuditLog.objects.create(
                        user=request.user,
                        action=request.method.lower(),
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
                    )
            except Exception:
                pass