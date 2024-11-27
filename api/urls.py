from django.urls import path
from api import views


urlpatterns = [
    path('', views.get_routes),
    path('entries/', views.get_entries),
    path('entries/<int:pk>/', views.get_entry),
]
