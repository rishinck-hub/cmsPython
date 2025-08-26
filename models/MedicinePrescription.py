class MedicinePrescription:
    def __init__(self,medicine_prescription_id=None,medicine_id=None,dosage=None,frequency=None,duration=None,quantity=None,appointmnent_id=None):
        self.__medicine_prescription_id = medicine_prescription_id
        self.__medicine_id = medicine_id
        self.__dosage = dosage
        self.__frequency = frequency
        self.__duration = duration
        self.__quantity = quantity
        self.__appointment_id = appointmnent_id

    @property
    def medicine_prescription_id(self):
        return self.__medicine_prescription_id
    
    @property
    def medicine_id(self):
        return self.__medicine_id
    @medicine_id.setter
    def medicine_id(self,value):
        self.__medicine_id = value

    @property
    def dosage(self):
        return self.__dosage 
    @dosage.setter
    def dosage(self,value):
        self.__dosage = value

    @property
    def frequency(self):
        return self.__frequency
    @frequency.setter
    def frequency(self,value):
        self.__frequency = value

    @property
    def duration(self):
        return self.__duration
    @duration.setter
    def duration(self,value):
        self.__duration = value

    @property
    def  quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self,value):
        self.__quantity = value

    @property
    def appointment_id(self):
        return self.__appointment_id
    @appointment_id.setter
    def appointment_id(self,value):
        self.__appointment_id = value

    def __str__(self):
        return f'Medicine prescription ID :{self.__medicine_prescription_id},\tMedicine ID :{self.__medicine_id},\tDosage :{self.__dosage},Frequency :{self.__frequency},\tDuration :{self.__duration},\tQuantity :{self.__quantity},\tAppointment ID :{self.__appointment_id}'