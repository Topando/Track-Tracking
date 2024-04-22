from authentication import views

from django.urls import path

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='user_register'),
    path('login/', views.LoginUserView.as_view(), name='user_login'),
    path('confirm-email/', views.CheckEmailView.as_view(), name='email_confirmation'),
]
