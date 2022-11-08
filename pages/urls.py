from django.urls import path
import os
import sys
from . import views

urlpatterns = [
    path('', views.Main.as_view(), name='home'),
    path('printerstats/<str:place>', views.printerstats,name='printerstats'),
    path('cartridge_stats', views.cartridge_stats, name = 'cartridge_stats'),
    path('cartridge_stats/add', views.give_cartridge, name = 'give_cartridge'),
    path('cartridge_stats/delete/<int:pk>', views.delete_data, name = 'cartridge_delete'),
    path('cartridge_stats/update/<int:pk>', views.update_data, name = 'cartridge_update'),
    path('drum_stats', views.drum_stats, name = 'drum_stats'),
    path('drum_stats/add', views.give_drum, name = 'give_drum'),
    path('drum_stats/delete/<int:pk>', views.delete_drum, name = 'drum_delete'),
    path('drum_stats/update/<int:pk>', views.update_drum, name = 'drum_update'),
    path('view_full_report', views.view_full_report, name='view_full_report'),
    path('cartridge_utility', views.cartridge_utility, name='cartridge_utility'),
    path('request_printers',views.request_printers_stats,name='request_printers'),
    path('obmen',views.obmen, name='obmen'),
    path('obmen/update/<int:pk>', views.obmen_update,name='obmen_update'),
    path('obmen/get', views.folders_api,name='get'),

]