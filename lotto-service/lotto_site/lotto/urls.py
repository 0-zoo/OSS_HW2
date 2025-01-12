# lotto_site/lotto/urls.py
from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지
    path('purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('purchase_result/', views.purchase_result, name='purchase_result'),
    path('draw/', views.draw_winning_numbers, name='draw_winning_numbers'),
    path('results/', views.check_result, name='check_result'),
    path('statistics/', views.statistics, name='statistics'),
]
