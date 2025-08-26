from abc import ABC, abstractmethod
from typing import List
from models.Consultation import Consultation

class ConsultationDaoService(ABC):
    @abstractmethod
    def display_all_consultations(self) -> List[Consultation]:
        '''Display all consultations'''
        pass

    @abstractmethod
    def insert_consultation(self, consultation: Consultation) -> bool:
        '''Insert a consultation'''
        pass

    @abstractmethod
    def find_by_consultation_id(self, consultation_id: int) -> Consultation:
        '''Find a consultation by ID'''
        pass

    @abstractmethod
    def update_consultation(self, consultation: Consultation, consultation_id: int) -> bool:
        '''Update a consultation by ID'''
        pass

    @abstractmethod
    def delete_consultation(self, consultation: Consultation, consultation_id: int) -> bool:
        '''Delete a consultation'''
        pass

    @abstractmethod
    def display_consultation(self, consultation: Consultation, consultation_id: int) -> Consultation:
        '''Display a consultation'''
        pass
