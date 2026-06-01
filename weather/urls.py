from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/weather/', views.fetch_weather_api, name='fetch_weather_api'),
    path('api/location/save/', views.save_location_api, name='save_location_api'),
    path('api/location/delete/<int:location_id>/', views.delete_location_api, name='delete_location_api'),
]
