from django.urls import path

from authentication import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='user_register'),
    path('login/', views.LoginUserView.as_view(), name='user_login'),
    path('confirm-email/<str:uidb64>/<str:token>/', views.CheckEmailView.as_view(), name='email_confirmation'),
]