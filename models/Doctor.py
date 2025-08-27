class Doctor:
    def __init__(self, doctorid=None, consultation_fee=None, specializationid=None,
                 staffid=None, isactive=True):
        self.__doctorid = doctorid
        self.__consultation_fee = consultation_fee
        self.__specializationid = specializationid
        self.__staffid = staffid
        self.__isactive = isactive

    # --- doctorid ---
    @property
    def doctorid(self):
        return self.__doctorid

    @doctorid.setter
    def doctorid(self, value):
        self.__doctorid = value

    # --- consultation_fee ---
    @property
    def consultation_fee(self):
        return self.__consultation_fee

    @consultation_fee.setter
    def consultation_fee(self, fee):
        if fee is not None and fee < 0:
            raise ValueError(" Consultation fee cannot be negative")
        self.__consultation_fee = fee

    # --- specializationid ---
    @property
    def specializationid(self):
        return self.__specializationid

    @specializationid.setter
    def specializationid(self, value):
        self.__specializationid = value

    # --- staffid ---
    @property
    def staffid(self):
        return self.__staffid

    @staffid.setter
    def staffid(self, value):
        self.__staffid = value

    # --- isactive ---
    @property
    def isactive(self):
        return self.__isactive

    @isactive.setter
    def isactive(self, value):
        self.__isactive = value

    # --- utility ---
    def __str__(self):
        return (
                f"DoctorID        : {self.__doctorid}\n"
                f"Consultation Fee: {self.__consultation_fee}\n"
                f"SpecializationID: {self.__specializationid}\n"
                f"StaffID         : {self.__staffid}\n"
                f"IsActive        : {self.__isactive}"
          )