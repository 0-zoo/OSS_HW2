# lotto_site/lotto/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('draw/', views.draw_winning_numbers, name='draw_winning_numbers'),
    path('results/', views.check_result, name='check_result'),
    path('statistics/', views.statistics, name='statistics'),
]
