from rest_framework import generics, permissions
from .models import AuditLog


class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return AuditLog.objects.all()
        return AuditLog.objects.filter(user=self.request.user)