from django.urls import path
from . import views

urlpatterns = [
    path('location/', views.get_location_details, name="location"),
    path('find/', views.get_corordinates, name='coordinates')
]
