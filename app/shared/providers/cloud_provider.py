from abc import ABC, abstractmethod

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
    def list_resources(self) -> list:
        """Devuelve los recursos del proveedor como lista de ResourceDTO."""
        ...

    @abstractmethod
    def get_costs(self) -> list:
        """Devuelve los registros de coste como lista de CostDTO."""
        ...
        