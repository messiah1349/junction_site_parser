from app.client import Client
from app.backend import Backend
from constants.constants import TELEGRAM_TOKEN

backend = Backend()
client = Client(backend, TELEGRAM_TOKEN)
client.build_application()
