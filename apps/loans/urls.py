from django.urls import path
from .views import (
    LoanApplicationListCreateView, LoanApplicationDetailView,
    DocumentUploadView, DocumentListView
)

urlpatterns = [
    path('', LoanApplicationListCreateView.as_view(), name='loan-list-create'),
    path('<int:pk>/', LoanApplicationDetailView.as_view(), name='loan-detail'),
    path('<int:pk>/documents/', DocumentListView.as_view(), name='document-list'),
    path('<int:pk>/documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
]