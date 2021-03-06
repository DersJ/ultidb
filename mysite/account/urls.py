from django.urls import include, path
from account import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.loginview, name='main-view'),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('signup/', views.signup, name='signup'),
	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('password_change_done', views.passwordChangeDoneView, name='password_change_done'),


]