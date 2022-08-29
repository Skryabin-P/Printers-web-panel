from django.urls import path, include
import os
import sys
from . import views

urlpatterns = [
    # path('login/', views.login, name='login'),
    path('sign_up/', views.sign_up , name='sign_up'),
    path('', include("django.contrib.auth.urls")),
    path('', views.dashboard_main, name="dashboard_main"),
    path('<str:type>/', views.dashboard_type, name="dashboard_type"),
    path('<str:type>/<str:action>', views.add_new, name="dashboard_add"),
    path('<str:type>/delete/<int:pk>', views.delete_data, name="delete_data"),
    path('<str:type>/update/<int:pk>', views.update_data, name="update_data"),

]