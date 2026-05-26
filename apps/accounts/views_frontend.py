from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db import models
from django.utils import timezone
from apps.loans.models import LoanApplication, Prediction, Document
from apps.prediction.tasks import predict_loan_application


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user and user.status == 'active':
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or inactive account')
    
    return render(request, 'registration/login.html')


def register_view(request):
    if request.method == 'POST':
        from apps.accounts.forms import UserRegistrationForm
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.status = 'active'
            user.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        from apps.accounts.forms import UserRegistrationForm
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.is_applicant:
        total_applications = request.user.loan_applications.count()
        approved_count = request.user.loan_applications.filter(status='approved').count()
        pending_count = request.user.loan_applications.filter(status__in=['submitted', 'under_review']).count()
        
        return render(request, 'dashboard/applicant.html', {
            'total_applications': total_applications,
            'approved_count': approved_count,
            'pending_count': pending_count,
            'loans': request.user.loan_applications.all().order_by('-created_at')[:10],
        })
    else:
        return admin_dashboard_view(request)


@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff and not request.user.is_admin_role:
        return redirect('dashboard')
    
    applications = LoanApplication.objects.all()
    predictions = Prediction.objects.all()
    
    stats = {
        'total_applications': applications.count(),
        'approved': applications.filter(status='approved').count(),
        'rejected': applications.filter(status='rejected').count(),
        'pending': applications.filter(status__in=['submitted', 'under_review']).count(),
        'avg_credit_score': applications.aggregate(avg=models.Avg('credit_score'))['avg'] or 0,
        'avg_loan_amount': applications.aggregate(avg=models.Avg('amount'))['avg'] or 0,
        'approval_rate': round(applications.filter(status='approved').count() / max(applications.count(), 1) * 100, 1),
    }
    
    risk_distribution = {'low': 0, 'medium': 0, 'high': 0}
    for pred in predictions:
        if pred.risk_level in risk_distribution:
            risk_distribution[pred.risk_level] += 1
    
    return render(request, 'dashboard/admin.html', {
        'stats': stats,
        'recent_applications': applications.select_related('user').prefetch_related('prediction').order_by('-created_at')[:10],
        'risk_distribution': risk_distribution,
    })


@login_required
def loan_list_view(request):
    loans = request.user.loan_applications.all().order_by('-created_at')
    return render(request, 'loans/loan_list.html', {'loans': loans})


@login_required
def loan_create_view(request):
    if request.method == 'POST':
        from apps.loans.forms import LoanApplicationForm
        form = LoanApplicationForm(request.POST, request.FILES)
        
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.status = 'submitted'
            loan.save()
            
            for doc_type in ['income_proof', 'identity_proof', 'address_proof']:
                if doc_type in request.FILES:
                    from apps.loans.models import Document
                    Document.objects.create(
                        application=loan,
                        file=request.FILES[doc_type],
                        document_type=doc_type,
                        original_filename=request.FILES[doc_type].name
                    )
            
            prediction_created = False
            try:
                predict_loan_application.delay(loan.id)
                prediction_created = True
            except Exception:
                try:
                    predict_loan_application(loan.id)
                    prediction_created = True
                except Exception as e:
                    messages.warning(request, f'Application saved but prediction could not be generated: {str(e)}')
            
            if prediction_created:
                messages.success(request, 'Application submitted successfully. Prediction generated.')
            
            return redirect('loan-detail', pk=loan.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        from apps.loans.forms import LoanApplicationForm
        form = LoanApplicationForm()
    
    return render(request, 'loans/application_form.html', {'form': form})


@login_required
def loan_detail_view(request, pk):
    loan = LoanApplication.objects.select_related('prediction').get(pk=pk)
    if loan.user != request.user and not request.user.is_staff:
        return redirect('dashboard')
    
    prediction = None
    if hasattr(loan, 'prediction') and loan.prediction:
        prediction = loan.prediction
    elif loan.status == 'submitted':
        try:
            from apps.prediction.tasks import predict_loan_application
            predict_loan_application(loan.id)
            prediction = loan.prediction if hasattr(loan, 'prediction') else None
        except Exception:
            pass
    
    return render(request, 'loans/loan_detail.html', {'loan': loan, 'prediction': prediction})


@login_required
def loan_delete_view(request, pk):
    loan = LoanApplication.objects.get(pk=pk)
    if loan.user != request.user and not request.user.is_staff:
        return redirect('dashboard')
    
    if request.method == 'POST':
        loan.delete()
        messages.success(request, 'Loan application deleted successfully.')
        return redirect('loan-list')
    
    return render(request, 'loans/loan_confirm_delete.html', {'loan': loan})


@login_required
def loan_review_view(request, pk):
    if not request.user.is_loan_officer and not request.user.is_credit_analyst:
        return redirect('dashboard')
    
    loan = LoanApplication.objects.get(pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['approved', 'rejected']:
            loan.status = new_status
            loan.reviewed_by = request.user
            loan.reviewed_at = timezone.now()
            loan.save()
            messages.success(request, f'Application {new_status}')
            return redirect('admin-dashboard')
    
    return render(request, 'loans/review.html', {'loan': loan})