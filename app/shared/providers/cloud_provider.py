from abc import ABC, abstractmethod
from app.shared.providers.schemas import ScopeDTO, ResourceDTO

class CloudProvider(ABC):
    """Interfaz común para todos los proveedores cloud (Azure, AWS, GCP).

    Cada proveedor implementa esta ABC. Los métodos devuelven DTOs definidos en
    app/shared/providers/schemas.py, nunca modelos ORM directamente.
    """

    @abstractmethod
    def verify_credentials(self) -> bool:
        """Comprueba que las credenciales son válidas. Devuelve True si la autenticación tiene éxito."""
        ...


    @abstractmethod
    def get_scopes(self) -> list[ScopeDTO]:
        """Devuelve la jerarquía de ámbitos del proveedor, aplanada como lista de ScopeDTO.

        Un ámbito es cualquier nivel organizativo que agrupa recursos. Cada proveedor
        mapea su propia jerarquía a ScopeDTO (p. ej. en Azure: tenant → suscripción →
        grupo de recursos). La relación padre/hijo se expresa con ScopeDTO.padre_ref_id.
        """

    @abstractmethod
    def list_resources(self) -> list:
        """Devuelve los recursos del proveedor como lista de ResourceDTO."""
        ...

    @abstractmethod
    def get_costs(self) -> list:
        """Devuelve los registros de coste como lista de CostDTO."""
        ...
        