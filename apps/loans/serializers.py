from rest_framework import serializers
from .models import LoanApplication, Document, Prediction


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'document_type', 'original_filename', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'probability_score', 'risk_level', 'recommendation', 'confidence', 'model_version', 'created_at']
        read_only_fields = ['id', 'created_at']


class LoanApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    prediction = PredictionSerializer(read_only=True)
    debt_to_income_ratio = serializers.FloatField(read_only=True)
    loan_to_income_ratio = serializers.FloatField(read_only=True)
    
    class Meta:
        model = LoanApplication
        fields = [
            'id', 'amount', 'tenure', 'employment_status', 'monthly_income', 'monthly_expense',
            'credit_score', 'existing_loans', 'existing_emis', 'status', 'purpose',
            'additional_info', 'debt_to_income_ratio', 'loan_to_income_ratio',
            'documents', 'prediction', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LoanApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = [
            'amount', 'tenure', 'employment_status', 'monthly_income', 'monthly_expense',
            'credit_score', 'existing_loans', 'existing_emis', 'purpose', 'additional_info'
        ]


class LoanApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['status']


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_type', 'file']