import os
import requests
import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import SavedLocation
from reminders.models import WeatherAlertRule

@login_required
def dashboard(request):
    saved_locations = SavedLocation.objects.filter(user=request.user)
    # Generate verification link for telegram bot
    profile = request.user.profile
    verif_code = profile.generate_verification_code()
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot_username = "AI_Weather_Alert_Bot" # Default or customizable
    
    # We can fetch bot username from telegram bot API, but default is fine.
    telegram_link = f"https://t.me/{bot_username}?start={verif_code}" if bot_token else "#"
    
    # List rules for each saved location
    locations_data = []
    for loc in saved_locations:
        rule = WeatherAlertRule.objects.filter(location=loc, user=request.user).first()
        if not rule:
            rule = WeatherAlertRule.objects.create(location=loc, user=request.user)
        locations_data.append({
            'location': loc,
            'rule': rule
        })

    context = {
        'locations_data': locations_data,
        'telegram_link': telegram_link,
        'telegram_code': verif_code,
        'telegram_linked': profile.telegram_chat_id is not None,
        'has_api_key': bool(os.getenv('OPENWEATHER_API_KEY')),
    }
    return render(request, 'weather/dashboard.html', context)

def fetch_weather_api(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if not lat or not lon:
        return JsonResponse({'error': 'Coordinates required'}, status=400)
        
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        # Fallback to realistic mock data if API key is not set
        lat_f = float(lat)
        lon_f = float(lon)
        # Mock weather variation based on coordinates
        temp = round(20.0 + (lat_f % 15) - (lon_f % 10), 1)
        humidity = int(50 + (lat_f * 3 + lon_f) % 40)
        wind_speed = round(1.5 + (lat_f * 2) % 15, 1)
        
        weather_conditions = [
            {'main': 'Clear', 'description': 'clear sky', 'icon': '01d'},
            {'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'},
            {'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'},
            {'main': 'Thunderstorm', 'description': 'thunderstorm with rain', 'icon': '11d'},
            {'main': 'Drizzle', 'description': 'light intensity drizzle', 'icon': '09d'}
        ]
        condition = weather_conditions[int((lat_f + lon_f) * 100) % len(weather_conditions)]
        
        return JsonResponse({
            'is_mock': True,
            'name': f"Region ({round(lat_f, 3)}, {round(lon_f, 3)})",
            'main': {
                'temp': temp,
                'feels_like': round(temp + 1.2, 1),
                'humidity': humidity,
                'pressure': 1012
            },
            'wind': {
                'speed': wind_speed
            },
            'weather': [condition]
        })
        
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&amp;lon={lon}&amp;appid={api_key}&amp;units=metric"
        # Wait, the url parameters have standard & character. Make sure they are not double-escaped.
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            data['is_mock'] = False
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Failed to fetch from OpenWeather', 'status_code': response.status_code}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def save_location_api(request):
    import json
    try:
        data = json.loads(request.body)
        name = data.get('name')
        lat = data.get('lat')
        lon = data.get('lon')
        
        if not name or lat is None or lon is None:
            return JsonResponse({'success': False, 'error': 'Missing fields'}, status=400)
            
        location, created = SavedLocation.objects.get_or_create(
            user=request.user,
            latitude=round(float(lat), 6),
            longitude=round(float(lon), 6),
            defaults={'name': name}
        )
        
        # Create corresponding alert rule
        rule, rule_created = WeatherAlertRule.objects.get_or_create(
            user=request.user,
            location=location
        )
        
        return JsonResponse({
            'success': True,
            'created': created,
            'location': {
                'id': location.id,
                'name': location.name,
                'latitude': float(location.latitude),
                'longitude': float(location.longitude)
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def delete_location_api(request, location_id):
    try:
        location = SavedLocation.objects.get(id=location_id, user=request.user)
        location.delete()
        return JsonResponse({'success': True})
    except SavedLocation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Location not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
