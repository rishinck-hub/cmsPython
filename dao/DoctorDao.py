from abc import ABC, abstractmethod
from typing import List
from models.Doctor import Doctor

class DoctorDaoService(ABC):

    @abstractmethod
    def insert_doctor(self, doctor: Doctor) -> bool:
        pass

    @abstractmethod
    def display_all_doctors(self) -> List[Doctor]:
        pass

    @abstractmethod
    def find_by_id(self) -> List[Doctor]:
        pass

    @abstractmethod
    def disable_doctor(self) ->List[Doctor]:
        pass
                                    