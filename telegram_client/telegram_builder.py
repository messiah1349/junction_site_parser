from telegram_client.app.client import Client
from telegram_client.app.backend import Backend
from constants.constants import TELEGRAM_TOKEN

backend = Backend()
client = Client(backend, TELEGRAM_TOKEN)
# client.build_application()
