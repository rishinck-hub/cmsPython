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
    def symptoms(self,value):
        self.__symptoms = value


    @property
    def diagnosis(self):
        return self.__diagnosis
    @diagnosis.setter
    def diagnosis(self,value):
        self.__diagnosis = value

    
    @property
    def created_date(self):
        return self.__created_date
    @created_date.setter
    def created_date(self,value):
        self.__created_date = value

    @property
    def appointment_id(self):
        return self.__appointment_id
    @appointment_id.setter
    def appointment_id(self,value):
        self.__appointment_id = value


    def __str__(self):
        return f'Consultation ID :{self.__consultation_id}\tSymptoms :{self.__symptoms},\tDiagnosis :{self.__diagnosis},\tCreated date :{self.__created_date},\tAppointment ID :{self.__appointment_id}'