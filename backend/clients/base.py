from abc import ABC, abstractmethod
class BaseClient(ABC):
    name:str
    @abstractmethod
    async def generate(self,prompt:str)->str:...
