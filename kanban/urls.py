"""
URL configuration for kanban project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home_page

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
API_TITLE = 'KanBan App API Documentations' # new
API_DESCRIPTION = 'REST API for kanban'
# schema_view = get_schema_view(title=API_TITLE)

schema_view = get_schema_view(
   openapi.Info(
      title="Kanban App API Documentations",
      default_version='v1',
      description="REST API v1",
      contact=openapi.Contact(email="indra.khanal@cotiviti.com"),
      license=openapi.License(name="GNU License"),
      terms_of_service="http://65.0.18.97/swagger/policies/terms/",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('', home_page, name="home"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
