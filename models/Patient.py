from lib.PatientManagementLib import PatientManagementLib

class Patient:
    def __init__(self, patient_id: int | None, name: str, dob: str, gender: str, bloodgroup: str, mobile_no: str, address: str, is_active: bool = True):
        # Validate all parameters before setting them
        # patient_id can be None for auto-increment inserts
        if patient_id is not None and not PatientManagementLib.validate_patient_id(patient_id):
            raise ValueError("Invalid patient ID")
        if not PatientManagementLib.validate_name(name):
            raise ValueError("Invalid patient name")
        if not PatientManagementLib.validate_dob(dob):
            raise ValueError("Invalid date of birth")
        if not PatientManagementLib.validate_gender(gender):
            raise ValueError("Invalid gender")
        if not PatientManagementLib.validate_bloodgroup(bloodgroup):
            raise ValueError("Invalid blood group")
        if not PatientManagementLib.validate_mobile(mobile_no):
            raise ValueError("Invalid mobile number")
        if not PatientManagementLib.validate_address(address):
            raise ValueError("Invalid address")
        if not isinstance(is_active, bool):
            raise ValueError("is_active must be a boolean")
            
        self.__patientid = patient_id
        self.__name = name.strip()
        self.__dob = dob
        self.__gender = gender.lower()
        self.__bloodgroup = bloodgroup.strip().upper()
        self.__mobileno = mobile_no
        self.__address = address.strip()
        self.__isactive = is_active

    def get_patientid(self): return self.__patientid
    def get_name(self): return self.__name
    def get_dob(self): return self.__dob
    def get_gender(self): return self.__gender
    def get_bloodgroup(self): return self.__bloodgroup
    def get_mobileno(self): return self.__mobileno
    def get_address(self): return self.__address
    def get_isactive(self): return self.__isactive

    def set_name(self, name): 
        if not PatientManagementLib.validate_name(name):
            raise ValueError("Invalid patient name")
        self.__name = name.strip()
        
    def set_dob(self, dob): 
        if not PatientManagementLib.validate_dob(dob):
            raise ValueError("Invalid date of birth")
        self.__dob = dob
        
    def set_gender(self, gender): 
        if not PatientManagementLib.validate_gender(gender):
            raise ValueError("Invalid gender")
        self.__gender = gender.lower()
        
    def set_bloodgroup(self, bloodgroup):
        if not PatientManagementLib.validate_bloodgroup(bloodgroup):
            raise ValueError("Invalid blood group")
        self.__bloodgroup = bloodgroup.strip().upper()
        
    def set_mobileno(self, mobile_no): 
        if not PatientManagementLib.validate_mobile(mobile_no):
            raise ValueError("Invalid mobile number")
        self.__mobileno = mobile_no
        
    def set_address(self, address): 
        if not PatientManagementLib.validate_address(address):
            raise ValueError("Invalid address")
        self.__address = address.strip()
        
    def set_isactive(self, is_active): 
        if not isinstance(is_active, bool):
            raise ValueError("is_active must be a boolean")
        self.__isactive = is_active

    def __str__(self):
        return (
            f"Patient[ID={self.__patientid}, Name={self.__name}, Gender={self.__gender}, "
            f"BloodGroup={self.__bloodgroup}, Mobile={self.__mobileno}, Address={self.__address}]"
        )
