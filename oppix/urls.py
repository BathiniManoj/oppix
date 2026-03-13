# """
# URL configuration for oppix project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/6.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import include, path
# from django.conf import settings
# from django.conf.urls.static import static
# from resumes.views import upload_resume
# from opportunities.views import opportunities
# #from applications.views import apply_opportunity

# urlpatterns = [
    
#     path('app/', include('app.urls')),  # Prefix app1 URLs with /app/
#     path('resumes/', include('resumes.urls')),  # Prefix resumes URLs with /resumes/
#     path('applications/', include('applications.urls')),  # Prefix applications URLs with /applications/
#     path('opportunities/', include('opportunities.urls')),  # Prefix opportunities URLs with /opportunities/

#     path('admin/', admin.site.urls),
#     path("upload-resume/", upload_resume, name="upload_resume"),
#     path("opportunities/", opportunities, name="opportunities"),
#     #path("apply/<int:opp_id>/", apply_opportunity, name="apply"),
# ]

# urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# oppix/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Direct view imports
# from resumes.views import upload_resume
# from opportunities.views import opportunities
# from applications.views import apply_opportunity  # Uncomment once implemented

urlpatterns = [
    # Main app URLs
    path('', include('app.urls')),  # All URLs inside app/urls.py

    # Resume upload
    # path('upload-resume/', upload_resume, name='upload_resume'),

    # Opportunities
    # path('opportunities/', opportunities, name='opportunities'),
    # Add more opportunity URLs here when you create detail/category views

    # Applications (uncomment once you implement the view)
    # path('apply/<int:opp_id>/', apply_opportunity, name='apply'),

    # Admin
    path('admin/', admin.site.urls),
]

# Serve static and media files in development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)