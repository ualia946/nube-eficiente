from azure.identity import ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError
from app.shared.providers.cloud_provider import CloudProvider

class AzureProvider(CloudProvider):
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
        self._credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self._subscription = subscription_id
    
    @classmethod
    def from_credentials(cls, credentials: dict):
        return cls(
            tenant_id=credentials["tenant_id"],
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            subscription_id=credentials["subscription_id"]
        )
    
    def verify_credentials(self):
        try:
            token = self._credential.get_token("https://management.azure.com/.default")
            return True
        except ClientAuthenticationError as error:
            print(f"Error en la autentificación. Revisar credenciales: {error}")
            return False
    
    def list_resources(self):
        raise NotImplementedError
    
    def get_costs(self):
        raise NotImplementedError
    

            