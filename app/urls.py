from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importing Django's built-in login view

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('', views.home, name='home'),
    path('results/', views.job_results, name='job_results'),
    path('resumebuilder/', views.resumebuilder, name='resumebuilder'),
    path('atsresult/', views.atsresult, name='ats_result'),
    path('download/<int:resume_id>/', views.download_resume, name='download_resume'),

    # path('', views.home, name='home'),
    # path('register/', views.user_register, name='register'),
    # path('profile/', views.user_profile, name='profile'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),  # Add login URL
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add logout URL
    # path('opportunity/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    # path('category/<int:category_id>/', views.category_opportunities, name='category_opportunities'),
]