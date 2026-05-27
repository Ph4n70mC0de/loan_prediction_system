from django.db import models
from django.conf import settings


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('custom', 'Custom Report'),
    ]
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    data = models.JSONField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reports'


class KPI(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    target = models.FloatField()
    unit = models.CharField(max_length=20)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'kpis'