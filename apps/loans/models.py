from django.db import models
from django.conf import settings


class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('closed', 'Closed'),
    ]
    
    EMPLOYMENT_STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('self_employed', 'Self Employed'),
        ('unemployed', 'Unemployed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_applications')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure = models.PositiveIntegerField(help_text='Loan tenure in months')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES)
    years_employed = models.PositiveIntegerField(blank=True, null=True, help_text='Years in current employment')
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_expense = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.PositiveIntegerField()
    existing_loans = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    existing_emis = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    purpose = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_applications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Loan {self.id} - {self.amount} by {self.user.email}"
    
    @property
    def debt_to_income_ratio(self):
        if self.monthly_income > 0:
            return (self.monthly_expense + self.existing_emis) / self.monthly_income
        return 0
    
    @property
    def loan_to_income_ratio(self):
        if self.monthly_income > 0:
            return self.amount / (self.monthly_income * 12)
        return 0


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('income_proof', 'Income Proof'),
        ('identity_proof', 'Identity Proof'),
        ('address_proof', 'Address Proof'),
        ('credit_report', 'Credit Report'),
        ('employment_letter', 'Employment Letter'),
        ('bank_statement', 'Bank Statement'),
        ('other', 'Other'),
    ]
    
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'documents'
    
    def __str__(self):
        return f"{self.document_type} for Loan {self.application.id}"


class Prediction(models.Model):
    RISK_LEVEL_CHOICES = [
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ]
    
    RECOMMENDATION_CHOICES = [
        ('approve', 'Approve'),
        ('review', 'Review'),
        ('reject', 'Reject'),
    ]
    
    application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='prediction')
    probability_score = models.FloatField(help_text='Probability of approval (0-1)')
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    recommendation = models.CharField(max_length=10, choices=RECOMMENDATION_CHOICES)
    confidence = models.FloatField(help_text='Model confidence score')
    model_version = models.CharField(max_length=50)
    feature_importance = models.JSONField(blank=True, null=True)
    shap_values = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'predictions'
    
    def __str__(self):
        return f"Prediction for Loan {self.application.id} - {self.risk_level}"