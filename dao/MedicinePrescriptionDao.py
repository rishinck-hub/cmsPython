from abc import ABC, abstractmethod
from typing import List
from models.MedicinePrescription import MedicinePrescription

class MedicinePrescriptionDaoService(ABC):
    @abstractmethod
    def display_all_prescriptions(self) -> List[MedicinePrescription]:
        '''Display all prescriptions'''
        pass

    @abstractmethod
    def insert_prescription(self, prescription: MedicinePrescription) -> bool:
        '''Insert a prescription'''
        pass

    @abstractmethod
    def find_by_id(self, prescription_id: int) -> MedicinePrescription:
        '''Find a prescription by ID'''
        pass

    @abstractmethod
    def update_prescription(self, prescription: MedicinePrescription, prescription_id: int) -> bool:
        '''Update a prescription by ID'''
        pass

    @abstractmethod
    def delete_prescription(self, prescription: MedicinePrescription, prescription_id: int) -> bool:
        '''Delete a prescription'''
        pass
