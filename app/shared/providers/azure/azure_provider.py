from azure.identity import ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError
from app.shared.providers.cloud_provider import CloudProvider

class AzureProvider(CloudProvider):
    """Implementación de CloudProvider para Microsoft Azure mediante service principal.

    Usa ClientSecretCredential (tenant_id + client_id + client_secret) de azure-identity.
    Construir con from_credentials() cuando las credenciales vienen de CuentaNube.credenciales.
    """

    def __init__(self, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
        self._credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self._subscription = subscription_id

    @classmethod
    def from_credentials(cls, credentials: dict):
        """Construye un AzureProvider desde el dict de credenciales de CuentaNube.

        El dict debe contener: tenant_id, client_id, client_secret, subscription_id.
        """
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
    

            