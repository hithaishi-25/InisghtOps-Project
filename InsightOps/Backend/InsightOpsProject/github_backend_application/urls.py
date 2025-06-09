from django.urls import path
from  . import views
urlpatterns = [
    # path('organization/<str:org_name>/', views.organization_detail, name='organization_detail'),
    #path('organization/', views.organization_detail, name='organization_detail'),
    path('organization/<str:org_name>/', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('home/',views.members,name="views")
]