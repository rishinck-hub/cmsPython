from abc import ABC, abstractmethod
from typing import List
from models.LabTestPrescription import LabTestPrescription

class LabTestPrescriptionDaoService(ABC):
    @abstractmethod
    def display_all_prescriptions(self) -> List[LabTestPrescription]:
        '''Display all Lab Test Prescriptions'''
        pass

    @abstractmethod
    def insert_prescription(self, prescription: LabTestPrescription) -> bool:
        '''Insert a new Lab Test Prescription'''
        pass

    @abstractmethod
    def find_by_id(self, labtest_prescription_id: int) -> LabTestPrescription:
        '''Find a Lab Test Prescription by ID'''
        pass

    @abstractmethod
    def update_prescription(self, prescription: LabTestPrescription, labtest_prescription_id: int) -> bool:
        '''Update a Lab Test Prescription by ID'''
        pass

    @abstractmethod
    def delete_prescription(self, prescription: LabTestPrescription, labtest_prescription_id: int) -> bool:
        '''Delete a Lab Test Prescription by ID'''
        pass
