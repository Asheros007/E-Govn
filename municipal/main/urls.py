from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('my_complaint/', views.my_complaint, name='my_complaint'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
]