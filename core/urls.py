from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/place-order/', views.place_order, name='place_order'),
    path('dashboard/place-quote/', views.place_quote, name='place_quote'),
    path('dashboard/update-profile/', views.update_profile, name='update_profile'),
    path('contact/', views.contact_submit, name='contact_submit'),
]
