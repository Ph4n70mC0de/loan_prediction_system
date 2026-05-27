from django.contrib import admin
from .models import LoanApplication, Document, Prediction


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'tenure', 'status', 'credit_score', 'created_at']
    list_filter = ['status', 'employment_status', 'created_at']
    search_fields = ['user__email', 'amount']
    ordering = ['-created_at']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'application', 'document_type', 'original_filename', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'application', 'risk_level', 'probability_score', 'recommendation', 'model_version']
    list_filter = ['risk_level', 'recommendation', 'model_version']