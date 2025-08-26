
# dao/medicine_dao_service.py
from abc import ABC, abstractmethod
from typing import List, Optional
from models.Medicine import Medicine  # assuming your Medicine class is here

class MedicineDaoService(ABC):
    @abstractmethod
    def display_all(self) -> List[Medicine]:
        """Return a list of all medicine records."""
        pass

    @abstractmethod
    def insert(self, med: Medicine) -> bool:
        """Insert a medicine; return True if successful."""
        pass

    @abstractmethod
    def find_by_id(self, medicineid: int) -> Optional[Medicine]:
        """Fetch a medicine by its ID."""
        pass

    @abstractmethod
    def update(self, med: Medicine, medicineid: int) -> bool:
        """Update the medicine identified by ID; return True if successful."""
        pass

    @abstractmethod
    def disable(self, medicineid: int) -> bool:
        """Disable (deactivate) a medicine by ID."""
        pass

    @abstractmethod
    def search(self, query: str) -> List[Medicine]:
        """Search medicines by name or category—case-insensitive."""
        pass

    @abstractmethod
    def apply_gst(self, medicineid: int, gst_percent: float) -> bool:
        """Apply GST to a given medicine's unit price; return True if successful."""
        pass
