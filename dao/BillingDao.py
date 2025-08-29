from abc import ABC, abstractmethod

class BillDAO(ABC):
    @abstractmethod
    def add_bill(self, bill): pass

    @abstractmethod
    def get_all_bills(self): pass

    @abstractmethod
    def get_bill_by_id(self, bill_id): pass
