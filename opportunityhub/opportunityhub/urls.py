"""
URL configuration for opportunityhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),  # Authentication endpoints
    path("api/youth/", include("youth_profiles.urls")),  # Youth profile endpoints
    path("api/opportunities/", include("opportunities.urls")),  # Opportunity endpoints
    path("api/employers/", include("employers.urls")),  # Employer profile endpoints
    path("api-auth/", include("rest_framework.urls")),  # DRF browsable API login
]
