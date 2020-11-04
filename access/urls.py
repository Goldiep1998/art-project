from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile', views.profile, name='profile'),
    path('deleteuser', views.delete_user, name='delete_user'),
    path('admin_delete_user/<int:id>', views.admin_delete_user, name='admin_delete_user')


]