from lib.AppointmentManagementLib import AppointmentManagementLib

class Appointment:
    def __init__(self, appointment_id: int, date: str, token_no: int, status: str, patient_id: int, doctor_id: int):
        # Validate all parameters before setting them
        if not AppointmentManagementLib.validate_appointment_id(appointment_id):
            raise ValueError("Invalid appointment ID")
        if not AppointmentManagementLib.validate_date(date):
            raise ValueError("Invalid appointment date")
        if not AppointmentManagementLib.validate_token_no(token_no):
            raise ValueError("Invalid token number")
        if not AppointmentManagementLib.validate_status(status):
            raise ValueError("Invalid appointment status")
        if not AppointmentManagementLib.validate_patient_id(patient_id):
            raise ValueError("Invalid patient ID")
        if not AppointmentManagementLib.validate_doctor_id(doctor_id):
            raise ValueError("Invalid doctor ID")
            
        self.__appointmentid = appointment_id
        self.__date = date
        self.__tokenno = token_no
        self.__status = status.lower()
        self.__patientid = patient_id
        self.__doctorid = doctor_id

    def get_appointmentid(self): return self.__appointmentid
    def get_date(self): return self.__date
    def get_tokenno(self): return self.__tokenno
    def get_status(self): return self.__status
    def get_patientid(self): return self.__patientid
    def get_doctorid(self): return self.__doctorid

    def set_date(self, date): 
        if not AppointmentManagementLib.validate_date(date):
            raise ValueError("Invalid appointment date")
        self.__date = date
        
    def set_tokenno(self, token_no): 
        if not AppointmentManagementLib.validate_token_no(token_no):
            raise ValueError("Invalid token number")
        self.__tokenno = token_no
        
    def set_status(self, status): 
        if not AppointmentManagementLib.validate_status(status):
            raise ValueError("Invalid appointment status")
        self.__status = status.lower()
        
    def set_patientid(self, patient_id): 
        if not AppointmentManagementLib.validate_patient_id(patient_id):
            raise ValueError("Invalid patient ID")
        self.__patientid = patient_id
        
    def set_doctorid(self, doctor_id): 
        if not AppointmentManagementLib.validate_doctor_id(doctor_id):
            raise ValueError("Invalid doctor ID")
        self.__doctorid = doctor_id

    def __str__(self):
        return f"Appointment[ID={self.__appointmentid}, Date={self.__date}, Token={self.__tokenno}, Status={self.__status}, PatientID={self.__patientid}]"
