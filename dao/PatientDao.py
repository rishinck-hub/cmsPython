from abc import ABC, abstractmethod

class PatientDao(ABC):
    @abstractmethod
    def add_patient(self, patient): pass

    @abstractmethod
    def list_patients(self): pass

    @abstractmethod
    def delete_patient(self, patient_id): pass

    @abstractmethod
    def update_patient(self, patient): pass
        
    @abstractmethod
    def update_patient_status(self, patient_id, is_active): pass
