from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('login/', UserLoginView, 'login')
# # router.register('login/refresh/', TokenRefreshView, 'refresh')
# router.register('user/create',RegisterView, 'create-user' )
app_name = 'users'


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', UserLoginView.as_view(), name="login"),
    path('api/register/', RegisterView.as_view(), name='register'),
    path("api/login/refresh", TokenRefreshView.as_view(), name="refresh"),
]
