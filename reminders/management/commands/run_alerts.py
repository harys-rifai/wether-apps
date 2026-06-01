from django.core.management.base import BaseCommand
from reminders.tasks import check_and_trigger_alerts

class Command(BaseCommand):
    help = 'Evaluates active weather alert rules and notifies users via Telegram of dangerous conditions'

    def handle(self, *args, **options):
        self.stdout.write('Starting weather alert evaluations...')
        try:
            stats = check_and_trigger_alerts()
            self.stdout.write(self.style.SUCCESS(
                f"Evaluation Completed Successfully!\n"
                f"- Rules Evaluated: {stats['evaluated']}\n"
                f"- Severe Matches Found: {stats['matched']}\n"
                f"- Telegram Warnings Sent: {stats['sent']}\n"
                f"- Active Cooldowns Skipped: {stats['skipped_cooldown']}\n"
                f"- Missing Telegram ID: {stats['no_telegram']}\n"
                f"- Processing Errors: {stats['errors']}"
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error during alert execution: {e}"))
