"""
URL configuration for django_strawberry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import os

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




from strawberry_app.views import (
    CultureAPI,
    MonthsAPI,
)

from strawberry_app import views
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

app_name = "strawberry_app"


urlpatterns = [
    # path('admin/', admin.site.urls),
    path(f"api/{os.getenv('API_VERSION')}/admin/", admin.site.urls),
    path(f"api/{os.getenv('API_VERSION')}/token", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f"api/{os.getenv('API_VERSION')}/token/refresh", TokenRefreshView.as_view(), name='token_refresh'),

    path(f"api/{os.getenv('API_VERSION')}/culture", CultureAPI.as_view()),
    path(f"api/{os.getenv('API_VERSION')}/culture/<culture_id>", CultureAPI.as_view()),
    path(f"api/{os.getenv('API_VERSION')}/months", MonthsAPI.as_view()),
    path(f"api/{os.getenv('API_VERSION')}/months/<months_id>", MonthsAPI.as_view()),


    path(f"api/{os.getenv('API_VERSION')}", views.register_request, name='start_page'),
    path(f"api/{os.getenv('API_VERSION')}/homepage", views.homepage, name='homepage'),
    path(f"api/{os.getenv('API_VERSION')}/register", views.register_request, name="register"),
    path(f"api/{os.getenv('API_VERSION')}/login", views.login_request, name="login"),
    path(f"api/{os.getenv('API_VERSION')}/logout", views.logout_request, name="logout"),
    path(f"api/{os.getenv('API_VERSION')}/profile", views.profile, name="profile"),
    path(f"api/{os.getenv('API_VERSION')}/search", views.search, name="search"),
    path(f"api/{os.getenv('API_VERSION')}/culture_list", views.culture_list, name="culture_list"),
    path(f"api/{os.getenv('API_VERSION')}/month_list", views.month_list, name="month_list"),
    path(f"api/{os.getenv('API_VERSION')}/calendar", views.year_calendar, name='calendar'),
    path(f"api/{os.getenv('API_VERSION')}/all_objects", views.all_objects_list, name='all_objects'),
    path(f"api/{os.getenv('API_VERSION')}/<int:year>/<int:month>/", views.month_detail, name='month_detail'),
    path(f"api/{os.getenv('API_VERSION')}/upload_images", views.upload_images, name="upload_images"),
    path(f"api/{os.getenv('API_VERSION')}/delete_file/<str:filename>/", views.delete_file, name='delete_file'),
    # path(f"api/{os.getenv('API_VERSION')}/choose_month/", views.choose_month, name='choose_month'),
    # path(f"api/{os.getenv('API_VERSION')}/choose_month/<int:month_id>", views.choose_month, name='choose_month'),

    path(f"api/{os.getenv('API_VERSION')}/choose_month/", views.choose_month, name='choose_month'),
    path(f"api/{os.getenv('API_VERSION')}/choose_month/<int:month_id>", views.choose_month,
         name='choose_month_with_id'),

    path(f"api/{os.getenv('API_VERSION')}/choose_culture/", views.choose_culture, name='choose_culture'),
    path(f"api/{os.getenv('API_VERSION')}/choose_culture/<int:culture_id>/", views.api_choose_culture,
         name='api_choose_culture_with_id'),
    path("api/<int:culture_id>/choose_culture/", views.api_choose_culture, name='api_choose_culture'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
