# # 🌦️ Weather Alert WebApp (Django + Telegram)

## 📌 Features
- **Frontend Map View**: Interactive weather map (OpenWeather + Leaflet.js).
- **Area Selection**: Users can select a region to view detailed weather.
- **Authentication**: Login system (Django Auth).with dasboard and sidebar menu glow neon blue
- **Dangerous Weather Alerts**: When severe conditions occur, reminders are sent via Telegram Bot.
- **Reminder Management**: Users can configure alerts after login.

## 🏗️ Project Structure

weather_app/
├── manage.py
├── weather_app/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/             # User login & auth
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── weather/              # Weather + Map logic
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── reminders/            # Telegram reminders
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   └── urls.py
└── static/               # JS, CSS, Leaflet assets

🚀 Workflow
1. User logs in → sees weather map.
2. Selects area → weather data fetched via OpenWeather API.
3. If dangerous weather → Telegram reminder sent.
4. User can manage reminders in dashboard.


# DB Configuration
Host: ep-blue-morning-am69itpc.c-5.us-east-1.aws.neon.tech
Database : notify, schema: machoneone
Role: neondb_owner
Password: npg_sfjvrTWXZw06
hostpooler: ep-blue-morning-am69itpc-pooler.c-5.us-east-1.aws.neon.tech


make run.sh to build and run this apps 
make push.sh to push to git:

git remote add origin https://github.com/harys-rifai/wether-apps.git
git branch -M main
git push -u origin main


