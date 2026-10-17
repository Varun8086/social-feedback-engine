from abc import ABC, abstractmethod
from backend.ingestion.models import RawPost

class BaseSource(ABC):
    @abstractmethod
    def fetch(self) -> list[RawPost]:
        """Return posts in the common RawPost shape."""