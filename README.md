# AI Weather App

A Django-based weather application with user accounts, saved locations, weather alerts, and Telegram integration.

## Features

### User Accounts
- Registration and login system
- User profiles with Telegram chat ID storage
- Automatic profile creation on user registration

### Weather Tracking
- Save multiple locations with name, latitude, and longitude
- View current weather and forecasts for saved locations
- Unique constraint prevents duplicate locations per user

### Weather Alerts
- Configure custom alert rules for each saved location
- Alert conditions:
  - Temperature high/low thresholds
  - Wind speed high threshold
  - Storm conditions
- Enable/disable individual alert types
- Track last alert sent time to prevent spam

### Telegram Integration
- Link Telegram account to user profile via verification code
- Receive weather alerts via Telegram bot
- Bot handles verification and alert delivery

## Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL database
- Telegram Bot Token (from @BotFather)
- OpenWeatherMap API key (for weather data)

### Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Unix/macOS: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env` file:
   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=*
   
   # Database (using local PostgreSQL)
   DB_HOST=127.0.0.1
   DB_NAME=notify
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_PORT=5432
   
   # APIs
   OPENWEATHER_API_KEY=your_openweather_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```
6. Apply migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`

### Running the Application
1. Start the development server: `python manage.py runserver`
2. Start the Telegram bot: `python manage.py run_telegram_bot`
3. Start the alert checker: `python manage.py run_alerts`

## Usage Guide

### 1. User Registration and Login
- Visit `/accounts/register/` to create a new account
- Log in at `/accounts/login/`
- After login, you'll be redirected to the weather dashboard

### 2. Managing Saved Locations
- On the dashboard, click "Add Location"
- Enter location name and coordinates (or use map interface if available)
- Saved locations appear in your list

### 3. Configuring Weather Alerts
- For each saved location, click "Configure Alerts"
- Set temperature high/low thresholds (in Celsius)
- Set wind speed threshold (in km/h or m/s - check unit in interface)
- Toggle alert types on/off
- Save your alert rules

### 4. Telegram Integration
- Go to your profile page
- Click "Link Telegram Account"
- Start a chat with your bot (use the token from @BotFather)
- Send the verification code shown in your profile
- Once verified, you'll receive weather alerts via Telegram

### 5. Checking Alerts
- The system automatically checks weather conditions for your saved locations
- When conditions match your alert rules, you'll receive notifications:
  - In-app notifications (if implemented)
  - Telegram messages (if Telegram is linked)

## Project Structure
- `accounts/` - User authentication and profiles
- `weather/` - Weather data models and views
- `reminders/` - Alert rules and Telegram bot functionality
- `templates/` - HTML templates for all apps
- `management/commands/` - Custom Django commands for bot and alert checker

## Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | `django-insecure-...` |
| DEBUG | Debug mode (True/False) | `True` |
| ALLOWED_HOSTS | Allowed hosts for Django | `*` |
| DB_HOST | Database host | `127.0.0.1` |
| DB_NAME | Database name | `notify` |
| DB_USER | Database user | `postgres` |
| DB_PASSWORD | Database password | `Password09` |
| DB_PORT | Database port | `5432` |
| OPENWEATHER_API_KEY | OpenWeatherMap API key | `your_key_here` |
| TELEGRAM_BOT_TOKEN | Telegram Bot token | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |

## Development
- Run tests: `python manage.py test`
- Check code style: `flake8` or `black .`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`

## Deployment
For production deployment:
1. Set `DEBUG=False`
2. Configure allowed hosts
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Set up HTTPS
5. Use environment variables for secrets
6. Consider using a process manager (systemd, supervisord) for background tasks

## Troubleshooting
- **Database connection errors**: Verify PostgreSQL is running and credentials in .env are correct
- **Telegram bot not responding**: Check bot token and ensure bot is started with `python manage.py run_telegram_bot`
- **Weather data not updating**: Verify OpenWeatherMap API key is valid and has sufficient quota
- **Alerts not triggering**: Check alert rules and verify weather data is being fetched correctly

## License
This project is proprietary software. All rights reserved.

## Contact
For support or inquiries, please refer to the project documentation.