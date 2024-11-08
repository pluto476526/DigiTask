from django.urls import path
from dash import views


urlpatterns = [
    path('', views.dash, name="dash"),
    path('categories/', views.categories, name="categories"),
    path('job_listings/', views.job_listings, name="job_listings"),
    path('my_posted_listings/', views.my_posted_listings, name="my_posted_listings"),
    path('my_applied_listings/', views.my_applied_listings, name="my_applied_listings"),
    path('short_tasks/', views.short_tasks, name="short_tasks"),
    path('feedback/', views.feedback, name="feedback"),
    path('job_details/<int:pk>', views.job_details, name="job_details"),
    path('pending_tasks/', views.pending_tasks, name="pending_tasks"),
    path('cancelled_tasks/', views.cancelled_tasks, name="cancelled_tasks"),
    path('ongoing_tasks/', views.ongoing_tasks, name="ongoing_tasks"),
]
