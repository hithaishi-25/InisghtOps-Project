from django.urls import path
from  . import views
urlpatterns = [
    path('organization/<str:org_name>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
]