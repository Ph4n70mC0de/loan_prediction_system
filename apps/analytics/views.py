from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from apps.loans.models import LoanApplication, Prediction
from .models import Report, KPI


class DashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        total_applications = LoanApplication.objects.count()
        approved = LoanApplication.objects.filter(status='approved').count()
        rejected = LoanApplication.objects.filter(status='rejected').count()
        pending = LoanApplication.objects.filter(status__in=['submitted', 'under_review']).count()
        
        avg_credit_score = LoanApplication.objects.aggregate(avg=Avg('credit_score'))['avg'] or 0
        avg_amount = LoanApplication.objects.aggregate(avg=Avg('amount'))['avg'] or 0
        
        risk_distribution = Prediction.objects.values('risk_level').annotate(count=Count('id'))
        
        return Response({
            'total_applications': total_applications,
            'approved': approved,
            'rejected': rejected,
            'pending': pending,
            'approval_rate': round(approved / total_applications * 100, 2) if total_applications > 0 else 0,
            'avg_credit_score': round(avg_credit_score, 2),
            'avg_loan_amount': round(avg_amount, 2),
            'risk_distribution': list(risk_distribution),
        })


class ReportListView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]


class KPIListView(generics.ListAPIView):
    queryset = KPI.objects.all()
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]