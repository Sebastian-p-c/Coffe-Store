from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType

# Establecer valores desde settings
Transaction.commerce_code = settings.TRANSBANK['commerce_code']
Transaction.api_key = settings.TRANSBANK['api_key']

# Selección del entorno según configuración
env = settings.TRANSBANK['environment'].lower()

if env == 'production':
    Transaction.integration_type = IntegrationType.LIVE
elif env == 'sandbox':
    Transaction.integration_type = IntegrationType.TEST
else:
    Transaction.integration_type = IntegrationType.MOCK  # opción segura por defecto
