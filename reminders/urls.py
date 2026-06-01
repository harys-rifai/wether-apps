from django.urls import path
from . import views

app_name = 'reminders'

urlpatterns = [
    path('api/rule/update/', views.update_rule_api, name='update_rule_api'),
    path('api/alerts/test/', views.trigger_test_alerts_api, name='trigger_test_alerts_api'),
]
