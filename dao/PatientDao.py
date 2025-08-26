from abc import ABC, abstractmethod

class PatientDao(ABC):
    @abstractmethod
    def add_patient(self, patient): pass

    @abstractmethod
    def list_patients(self): pass
