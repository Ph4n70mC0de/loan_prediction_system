from django.urls import path
from .views import DashboardView, ReportListView, KPIListView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('reports/', ReportListView.as_view(), name='reports'),
    path('kpis/', KPIListView.as_view(), name='kpis'),
]