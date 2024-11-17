from django.urls import path
from chats import views


urlpatterns = [
    path('', views.index_view, name="start_chats"),
    path('settings/', views.settings_view, name="settings"),
    path('text_messages/<str:username>/', views.text_messages, name="text_messages"),
]
