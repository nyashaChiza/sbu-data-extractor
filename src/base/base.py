from abc import ABC, abstractmethod


class BluePrint(ABC):
    """Abstract base class defining blueprint methods for CRUD operations."""
    
    @abstractmethod
    def get(self, pk: str):
        """Abstract method for retrieving data by primary key."""
        pass
    
    @abstractmethod
    def get_all(self):
        """Abstract method for retrieving all data."""
        pass
    
    @abstractmethod
    def post(self, pk: str):
        """Abstract method for posting a policy to the data source."""
        pass
    
    @abstractmethod
    def update(self, pk: str, data:dict):
        """Abstract method for updating a policy in the data source."""
        pass
    
    @abstractmethod
    def delete(self, pk: str):
        """Abstract method for delete a policy in the data source."""
        pass