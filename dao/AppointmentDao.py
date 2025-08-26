from abc import ABC, abstractmethod

class AppointmentDao(ABC):
    @abstractmethod
    def book_appointment(self, appointment): pass

    @abstractmethod
    def list_appointments(self): pass
