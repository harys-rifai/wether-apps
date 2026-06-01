import os
import requests
from django.utils import timezone
from django.contrib.auth.models import User
from .models import WeatherAlertRule
from weather.models import SavedLocation

def fetch_weather_for_task(lat, lon):
    """Helper to fetch weather for alert task, with mock fallback if API key is missing."""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        # Realistic mock weather based on lat/lon
        lat_f = float(lat)
        lon_f = float(lon)
        # Mock weather variation
        temp = round(20.0 + (lat_f % 15) - (lon_f % 10), 1)
        humidity = int(50 + (lat_f * 3 + lon_f) % 40)
        wind_speed = round(1.5 + (lat_f * 2) % 15, 1)
        
        weather_conditions = [
            {'main': 'Clear', 'description': 'clear sky'},
            {'main': 'Clouds', 'description': 'few clouds'},
            {'main': 'Rain', 'description': 'moderate rain'},
            {'main': 'Thunderstorm', 'description': 'thunderstorm with heavy rain'},
            {'main': 'Drizzle', 'description': 'light intensity drizzle'}
        ]
        condition = weather_conditions[int((lat_f + lon_f) * 100) % len(weather_conditions)]
        return {
            'temp': temp,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'main': condition['main'],
            'description': condition['description'],
            'is_mock': True
        }

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            d = res.json()
            return {
                'temp': d['main']['temp'],
                'humidity': d['main']['humidity'],
                'wind_speed': d['wind']['speed'],
                'main': d['weather'][0]['main'],
                'description': d['weather'][0]['description'],
                'is_mock': False
            }
    except Exception as e:
        print(f"Error fetching weather for alert: {e}")
    return None

def send_telegram_message(token, chat_id, text):
    """Sends a message to the user via Telegram Bot API."""
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown'
        }
        res = requests.post(url, json=payload, timeout=5)
        return res.status_code == 200
    except Exception as e:
        print(f"Failed to send Telegram warning: {e}")
        return False

def check_and_trigger_alerts(force_user=None):
    """
    Evaluates active rules, pulls weather data, and pushes alerts to Telegram.
    Can be filtered by a specific user (e.g. for dashboard-triggered tests).
    """
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    rules = WeatherAlertRule.objects.filter(is_active=True)
    if force_user:
        rules = rules.filter(user=force_user)
        
    stats = {
        'evaluated': 0,
        'matched': 0,
        'sent': 0,
        'errors': 0,
        'skipped_cooldown': 0,
        'no_telegram': 0
    }
    
    for rule in rules:
        stats['evaluated'] += 1
        
        # Check if user has Telegram Chat ID linked
        profile = getattr(rule.user, 'profile', None)
        if not profile or not profile.telegram_chat_id:
            stats['no_telegram'] += 1
            continue
            
        # Cooldown check: limit alerts to once every 5 minutes for easy testing/monitoring.
        # Can be adjusted for production if needed.
        if rule.last_alert_sent:
            time_since_alert = timezone.now() - rule.last_alert_sent
            if time_since_alert.total_seconds() < 300: # 5 minutes cooldown
                stats['skipped_cooldown'] += 1
                continue
                
        # Fetch current weather
        weather = fetch_weather_for_task(rule.location.latitude, rule.location.longitude)
        if not weather:
            stats['errors'] += 1
            continue
            
        # Check warning criteria
        triggers = []
        
        if rule.alert_on_temp_high and weather['temp'] >= float(rule.temp_high_threshold):
            triggers.append(f"Temperature high: {weather['temp']}°C (limit: {rule.temp_high_threshold}°C)")
            
        if rule.alert_on_temp_low and weather['temp'] <= float(rule.temp_low_threshold):
            triggers.append(f"Temperature low: {weather['temp']}°C (limit: {rule.temp_low_threshold}°C)")
            
        if rule.alert_on_wind_high and weather['wind_speed'] >= float(rule.wind_high_threshold):
            triggers.append(f"Wind speed high: {weather['wind_speed']} m/s (limit: {rule.wind_high_threshold} m/s)")
            
        if rule.alert_on_storm and weather['main'] in ['Thunderstorm', 'Tornado', 'Squall', 'Extreme', 'Rain']:
            # We also alert on Rain for storm alert if severe
            triggers.append(f"Dangerous weather conditions: {weather['main']} ({weather['description']})")
            
        if triggers:
            stats['matched'] += 1
            
            # Format and send Telegram Alert
            message = (
                f"🚨 *AI-WEATHER ALERT SYSTEM* 🚨\n\n"
                f"⚠️ *Severe Conditions Detected!*\n"
                f"📍 *Location:* {rule.location.name}\n"
                f"🌐 *Coords:* {rule.location.latitude}, {rule.location.longitude}\n\n"
                f"*Current Weather:*\n"
                f"• Temp: {weather['temp']}°C\n"
                f"• Wind: {weather['wind_speed']} m/s\n"
                f"• Conditions: {weather['description'].capitalize()}\n\n"
                f"*Triggers Activated:*\n" + "\n".join([f"• {t}" for t in triggers]) + "\n\n"
                f"_Please take necessary precautions._"
            )
            
            if weather['is_mock']:
                message += "\n\n_(Demo mode: Simulated weather data)_"
                
            if bot_token:
                success = send_telegram_message(bot_token, profile.telegram_chat_id, message)
                if success:
                    rule.last_alert_sent = timezone.now()
                    rule.save()
                    stats['sent'] += 1
                else:
                    stats['errors'] += 1
            else:
                # No bot token config, let's mock the send for validation
                print(f"Mocking alert send to Telegram chat {profile.telegram_chat_id}:\n{message}")
                rule.last_alert_sent = timezone.now()
                rule.save()
                stats['sent'] += 1 # Counted as sent for simulation purposes
                
    return stats
