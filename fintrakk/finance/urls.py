from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.transactions, name='transactions'),  # New Transactions View
    path('manage_accounts/', views.manage_accounts, name='manage_accounts'),
    path('edit_account/<int:account_id>/', views.edit_account, name='edit_account'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('get_report/', views.get_report, name='get_report'),
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('edit_transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
]