from azure.identity import ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError
from app.shared.providers.cloud_provider import CloudProvider
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient
from app.shared.providers.schemas import ScopeDTO, ResourceDTO

class AzureProvider(CloudProvider):
    """Implementación de CloudProvider para Microsoft Azure mediante service principal.

    Usa ClientSecretCredential (tenant_id + client_id + client_secret) de azure-identity.
    Construir con from_credentials() cuando las credenciales vienen de CuentaNube.credenciales.
    """

    def __init__(self, tenant_id: str, client_id: str, client_secret: str, subscription_id: str):
        self._tenant = tenant_id
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
    
    def get_scopes(self) -> list[ScopeDTO]:
        """Recorre la jerarquía del tenant y la devuelve aplanada como lista de ScopeDTO.

        Construye el árbol Tenant → Subscription → ResourceGroup: un nodo raíz para el
        tenant, un nodo por cada suscripción y un nodo por cada grupo de recursos. El
        padre_ref_id de cada DTO enlaza con el proveedor_ref_id de su padre, de modo que
        la capa de ingesta pueda reconstruir la jerarquía.

        Hace una llamada a la API de Azure por cada suscripción para listar sus grupos
        de recursos.
        """
        subscription_client = SubscriptionClient(self._credential)
        subs = subscription_client.subscriptions.list()
        
        scopes_dtos = []
        scopes_dtos.append(
            ScopeDTO(
                tipo_nodo="tenant",
                proveedor_ref_id=self._tenant,
                nombre=self._tenant,
                padre_ref_id=None
            )
        )
        
        for sub in subs:
            scopes_dtos.append(
                ScopeDTO(
                    tipo_nodo="subscription",
                    proveedor_ref_id=sub.subscription_id,
                    nombre=sub.display_name,
                    padre_ref_id=self._tenant
                )
            )

            resource_client = ResourceManagementClient(self._credential, sub.subscription_id)
            resource_groups = resource_client.resource_groups.list()

            for rg in resource_groups:
                scopes_dtos.append(
                    ScopeDTO(
                        tipo_nodo="resource_group",
                        proveedor_ref_id=rg.name,
                        nombre=rg.name,
                        padre_ref_id=sub.subscription_id
                    )
                )
        
        return scopes_dtos

        
        
    
    def list_resources(self):
        raise NotImplementedError
    
    def get_costs(self):
        raise NotImplementedError
    

            