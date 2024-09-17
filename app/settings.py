import os

from dotenv import load_dotenv

load_dotenv()


debug = False


STRIPE_SECRET_KEY = os.getenv('STRIPE_PROD')
# STRIPE_SECRET_KEY = os.getenv('STRIPE_TEST')

STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
