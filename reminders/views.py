import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import WeatherAlertRule
from weather.models import SavedLocation
from reminders.tasks import check_and_trigger_alerts

@login_required
@require_POST
def update_rule_api(request):
    try:
        data = json.loads(request.body)
        rule_id = data.get('rule_id')
        
        if not rule_id:
            return JsonResponse({'success': False, 'error': 'Rule ID required'}, status=400)
            
        rule = WeatherAlertRule.objects.get(id=rule_id, user=request.user)
        
        rule.alert_on_temp_high = data.get('alert_on_temp_high', rule.alert_on_temp_high)
        rule.temp_high_threshold = float(data.get('temp_high_threshold', rule.temp_high_threshold))
        
        rule.alert_on_temp_low = data.get('alert_on_temp_low', rule.alert_on_temp_low)
        rule.temp_low_threshold = float(data.get('temp_low_threshold', rule.temp_low_threshold))
        
        rule.alert_on_wind_high = data.get('alert_on_wind_high', rule.alert_on_wind_high)
        rule.wind_high_threshold = float(data.get('wind_high_threshold', rule.wind_high_threshold))
        
        rule.alert_on_storm = data.get('alert_on_storm', rule.alert_on_storm)
        rule.is_active = data.get('is_active', rule.is_active)
        
        rule.save()
        return JsonResponse({'success': True})
    except WeatherAlertRule.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Rule not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def trigger_test_alerts_api(request):
    try:
        # Run alert checker immediately and report results
        stats = check_and_trigger_alerts(force_user=request.user)
        return JsonResponse({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
