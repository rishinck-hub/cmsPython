class LabTestPrescription:
    def __init__(self,labtest_prescription_id=None,labtest_id=None,created_date=None,remarks=None,appointment_id=None):
        self.__labtest_prescription_id = labtest_prescription_id
        self.__labtest_id = labtest_id
        self.__created_date = created_date
        self.__remarks = remarks
        self.__appointment_id = appointment_id


    @property
    def labtest_prescription_id(self):
        return self.__labtest_prescription_id
    @labtest_prescription_id.setter
    def labtest_prescription_id(self,value):
        self.__labtest_prescription_id =value


    @property
    def labtest_id(self):
        return self.__labtest_id
    @labtest_id.setter
    def labtest_id(self,value):
        self.__labtest_id = value


    @property
    def created_date(self):
        return self.__created_date
    @created_date.setter
    def created_date(self,value):
        self.__created_date = value 

    @property
    def remarks(self):
        return self.__remarks
    @remarks.setter
    def remarks(self,value):
        self.__remarks = value
    @property
    def appointment_id(self):
        return self.__appointment_id
    @appointment_id.setter
    def appointment_id(self,value):
        self.__appointment_id = value

    def __str__(self):
        return f'Labtest Prescription ID :{self.__labtest_prescription_id},\tLabtest ID :{self.__labtest_id},\tCreated Date :{self.__created_date},\tRemarks :{self.__remarks},\tAppointment ID :{self.__appointment_id}'