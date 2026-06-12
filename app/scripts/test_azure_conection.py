import os
from dotenv import load_dotenv
from app.shared.providers.azure.azure_provider import AzureProvider

load_dotenv()

credentials = {
    "tenant_id": os.getenv("AZURE_TENANT_ID"),
    "client_id": os.getenv("AZURE_CLIENT_ID"),
    "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
    "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID"),
}

provider = AzureProvider.from_credentials(credentials)

if provider.verify_credentials():
    print("Conexión exitosa con Azure")
else:
    print("Conexión fallida")