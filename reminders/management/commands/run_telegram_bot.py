import os
import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Runs a long-polling listener to process linking requests from the Telegram Bot'

    def handle(self, *args, **options):
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            self.stderr.write(self.style.ERROR('TELEGRAM_BOT_TOKEN environment variable not set. Please configure it in .env'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting Telegram Bot Long-Polling Daemon...'))
        self.stdout.write(self.style.WARNING('Waiting for verification messages (/start <code>)... Press Ctrl+C to stop.'))
        
        offset = 0
        while True:
            try:
                # Long polling: wait up to 10 seconds for updates
                url = f"https://api.telegram.org/bot{bot_token}/getUpdates?offset={offset}&timeout=10"
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok') and data.get('result'):
                        for update in data['result']:
                            update_id = update['update_id']
                            offset = update_id + 1
                            
                            # Process message if present
                            if 'message' in update:
                                message = update['message']
                                chat_id = message['chat']['id']
                                text = message.get('text', '').strip()
                                
                                if text.startswith('/start'):
                                    self.process_start_command(bot_token, chat_id, text)
                                else:
                                    self.send_reply(bot_token, chat_id, "Welcome to AI-Weather Alerts!\n\nPlease link your dashboard account by typing:\n`/start <your_8_char_code>`\n\nYou can find this code in your Dashboard.")
                elif response.status_code == 401:
                    self.stderr.write(self.style.ERROR('Invalid TELEGRAM_BOT_TOKEN. Check your bot settings.'))
                    time.sleep(10)
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('\nTelegram Bot daemon stopped.'))
                break
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Connection error: {e}'))
                time.sleep(5)

    def process_start_command(self, token, chat_id, text):
        parts = text.split()
        if len(parts) < 2:
            msg = (
                "👋 *Welcome to AI-Weather Alert Bot!*\n\n"
                "To link this chat to your account and receive dangerous weather notifications:\n"
                "1. Log in to your AI-Weather dashboard.\n"
                "2. Copy your 8-character verification code.\n"
                "3. Send `/start <code>` to this bot here."
            )
            self.send_reply(token, chat_id, msg)
            return
            
        code = parts[1].strip()
        try:
            profile = UserProfile.objects.get(telegram_verification_code=code)
            profile.telegram_chat_id = str(chat_id)
            profile.save()
            
            msg = (
                f"✅ *Connection Successful!*\n\n"
                f"Your Telegram account has been linked to AI-Weather user: *{profile.user.username}*.\n\n"
                f"You will now receive severe weather alerts for your saved locations here."
            )
            self.send_reply(token, chat_id, msg)
            self.stdout.write(self.style.SUCCESS(f"Successfully linked user {profile.user.username} to chat {chat_id}"))
        except UserProfile.DoesNotExist:
            msg = "❌ *Invalid Verification Code.*\n\nPlease double check the code shown in your dashboard and try again."
            self.send_reply(token, chat_id, msg)

    def send_reply(self, token, chat_id, text):
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }, timeout=5)
        except Exception as e:
            self.stderr.write(f"Error sending reply: {e}")
