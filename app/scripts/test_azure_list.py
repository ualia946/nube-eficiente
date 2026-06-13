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

for dto in provider.get_scopes():
    print(f"{dto.tipo_nodo:20} | {dto.nombre:75} | padre: {dto.padre_ref_id}")