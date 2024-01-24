from django.urls import path
from .views import create_advertisement, respond_to_advertisement, dashboard, account_activation_sent, account_activation_invalid, advertisement_detail, edit_advertisement

urlpatterns = [
    path('create_advertisement/', create_advertisement, name='create_advertisement'),
    path('respond_to_advertisement/<int:advertisement_id>/', respond_to_advertisement, name='respond_to_advertisement'),
    path('dashboard/', dashboard, name='dashboard'),
    path('account/activation-sent/', account_activation_sent, name='account_activation_sent'),
    path('account/activation-invalid/', account_activation_invalid, name='account_activation_invalid'),
    path('advertisement/<int:pk>/', advertisement_detail, name='advertisement_detail'),
    path('advertisement/<int:pk>/edit/', edit_advertisement, name='edit_advertisement'),
]