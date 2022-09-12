from django.urls import path

from .views import login_view, RegisterView, logout_view, ProfileView

urlpatterns = [
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('register/', RegisterView.as_view(), name="register"),
  path('profile/', ProfileView.as_view(), name='profile'),
]