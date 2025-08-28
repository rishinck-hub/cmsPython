from abc import ABC, abstractmethod
from typing import List
from models.Staff import Staff

class LoginDaoService(ABC):
    @abstractmethod
    def get_staff_by_username(self, username: str):
        '''Impliment login functionality'''
        pass
    