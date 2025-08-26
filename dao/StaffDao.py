from abc import ABC, abstractmethod
from typing import List
from models.Staff import Staff

class StaffDaoService(ABC):
    @abstractmethod
    def insert_staff(self)->bool:
        pass

    @abstractmethod
    def display_all_staffs(self) -> List[Staff]:
        pass
    
    @abstractmethod
    def find_by_staffid(self, staffid: int) -> Staff:
      pass
    
    @abstractmethod
    def find_by_mobileno(self, mobileno: str) -> Staff:
      pass

    