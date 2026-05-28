from django import forms
from .models import LoanApplication, Document


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'amount', 'tenure', 'employment_status', 'years_employed',
            'monthly_income', 'monthly_expense', 'credit_score', 'existing_loans',
            'existing_emis', 'purpose', 'additional_info'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'min': 1000, 'step': 100}),
            'tenure': forms.NumberInput(attrs={'min': 1, 'max': 360}),
            'monthly_income': forms.NumberInput(attrs={'step': 100}),
            'monthly_expense': forms.NumberInput(attrs={'step': 100}),
            'credit_score': forms.NumberInput(attrs={'min': 300, 'max': 850}),
            'existing_emis': forms.NumberInput(attrs={'step': 100}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']