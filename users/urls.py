from django.urls import path
from .views import LoginView, ActivateAccountView, UserSessionView, LogoutView, SignUpView

urlpatterns=[
    path("login/", LoginView.as_view(), name="login"),
    path('activate/<str:uid>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('session', UserSessionView.as_view(), name="session"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    
]
