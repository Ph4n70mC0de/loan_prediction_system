from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('loan_officer', 'Loan Officer'),
        ('credit_analyst', 'Credit Analyst'),
        ('admin', 'Admin'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('pending_verification', 'Pending Verification'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_verification')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    @property
    def is_applicant(self):
        return self.role == 'applicant'
    
    @property
    def is_loan_officer(self):
        return self.role == 'loan_officer'
    
    @property
    def is_credit_analyst(self):
        return self.role == 'credit_analyst'
    
    @property
    def is_admin_role(self):
        return self.role == 'admin'
    
    @property
    def is_admin(self):
        return self.role == 'admin'