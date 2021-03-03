from django.urls import path

from . import views


urlpatterns = [
    path('alive/', views.alive, name='alive')
]
