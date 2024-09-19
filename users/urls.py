from django.urls import path, include
from .views import UserCreateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', include('dj_rest_auth.urls')),  # Login, Logout, Password Reset
    # path('register/', UserCreateView.as_view(), name='user-register'),
    path('registration/', include('dj_rest_auth.registration.urls')),  # User Registration
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]