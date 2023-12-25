from django.core.management.base import BaseCommand
from ... bot import start_telegram_bot

class Command(BaseCommand):
    help = 'Starts the Telegram bot using webhooks'

    def handle(self, *args, **options):
        start_telegram_bot()
