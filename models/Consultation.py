from datetime import date
class Consultation:
    def __init__(self,consultationid=None,symptoms=None,diagnosis=None,createddate=None,appointmentid=None):
        self.__consultation_id = consultationid
        self.__symptoms = symptoms
        self.__diagnosis = diagnosis
        self.__created_date = createddate
        self.__appointment_id = appointmentid

    @property
    def consultation_id(self):
        return self.__consultation_id
    
    @property
    def symptoms(self):
        return self.__symptoms
    @symptoms.setter
        