from abc import ABC, abstractmethod

class CloudProvider(ABC):
    @abstractmethod
    def verify_credentials(self) -> bool:
        ...
    
    @abstractmethod
    def list_resources(self) -> list:
        ...
    
    @abstractmethod
    def get_costs(self) -> list:
        ...
        