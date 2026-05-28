from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import LoanApplication, Document
from .serializers import (
    LoanApplicationSerializer, LoanApplicationCreateSerializer,
    DocumentUploadSerializer, DocumentSerializer
)
from apps.prediction.tasks import predict_loan_application


class LoanApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_applicant:
            return LoanApplication.objects.filter(user=user)
        return LoanApplication.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LoanApplicationCreateSerializer
        return LoanApplicationSerializer
    
    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user)
        predict_loan_application.delay(application.id)


class LoanApplicationDetailView(generics.RetrieveUpdateAPIView):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            if 'status' in self.request.data:
                from .serializers import LoanApplicationStatusUpdateSerializer
                return LoanApplicationStatusUpdateSerializer
        return LoanApplicationSerializer


class DocumentUploadView(generics.CreateAPIView):
    serializer_class = DocumentUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        application = generics.get_object_or_404(LoanApplication, id=self.kwargs['pk'])
        if application.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("Cannot upload documents for this application")
        serializer.save(
            application=application,
            original_filename=self.request.FILES['file'].name
        )


class DocumentListView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        application = generics.get_object_or_404(LoanApplication, id=self.kwargs['pk'])
        if application.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("Cannot view documents for this application")
        return application.documents.all()