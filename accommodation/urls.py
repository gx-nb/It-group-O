from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('check-out/create/', views.create_check_out_request, name='create_check_out'),
    path('check-out/review/<int:pk>/', views.review_check_out_request, name='review_check_out'),
    path('check-in/create/', views.create_check_in_record, name='create_check_in'),
    path('inspection/', views.inspection, name='inspection'),
path('inspection/fix/<int:pk>/', views.fix_inspection, name='fix_inspection'),
path('check-in/delete/<int:pk>/', views.delete_check_in, name='delete_check_in'),
path('check-out/edit/<int:pk>/', views.edit_check_out, name='edit_check_out'),
path('check-out/delete/<int:pk>/', views.delete_check_out, name='delete_check_out'),

path('inspection/edit/<int:pk>/', views.edit_inspection, name='edit_inspection'),
path('inspection/delete/<int:pk>/', views.delete_inspection, name='delete_inspection'),
path(
    "checkout/final/<int:pk>/",
    views.final_check_out,
    name="final_check_out"
),
path(
    'checkout/delete-admin/<int:pk>/',
    views.delete_checkout_admin,
    name='delete_checkout_admin'
),
path('check-in/edit/<int:pk>/', views.edit_check_in, name='edit_check_in'),
path("inspection/complete/<int:pk>/", views.complete_inspection, name="complete_inspection"),
]