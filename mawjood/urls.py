"""
URL configuration for mawjood project.

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
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import home, add_options, add_student, delete_sutudent, register_absence, register_attendance, register_presence, reset, error, auto_reports, reports
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include('Accounts.urls')),
    path("grades/", include('main.urls')),
    path("", home),
    path("add/", add_options),
    path("error/", error),
    path("reset/", reset),
    path('students/create', add_student),
    path('students/<int:id>/edit', add_student),
    path('students/<int:id>/delete', delete_sutudent),
    path('students/<int:id>/absent', register_absence),
    path('students/<int:id>/present', register_presence),
    path('students/classroom/<int:cid>/confirm_absence', register_attendance),
    path('students/classroom/<int:id>/generate_reports', auto_reports),
    path('students/<int:id>/reports', reports)

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

