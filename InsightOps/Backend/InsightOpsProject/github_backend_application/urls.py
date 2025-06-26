from django.urls import path
from  . import views
urlpatterns = [
    path('organization/<str:org_name>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization-metrics/', views.OrganizationMetricsView.as_view(), name='organization_metrics'),
]

