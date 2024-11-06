from django.urls import path
from public import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('sign_in', views.sign_in, name="sign_in"),
    path('sign_out', views.sign_out, name="sign_out"),
]
