class Bill:
    def __init__(self, bill_id, patient_id, appointment_id, medicine_prescription_id, labtest_prescription_id, 
                 consultation_fee=500.00, medicine_cost=0.00, labtest_cost=0.00, total_amount=None):
        self.__bill_id = bill_id
        self.__patient_id = patient_id
        self.__appointment_id = appointment_id
        self.__medicine_prescription_id = medicine_prescription_id
        self.__labtest_prescription_id = labtest_prescription_id
        self.__consultation_fee = consultation_fee
        self.__medicine_cost = medicine_cost
        self.__labtest_cost = labtest_cost
        # Total amount is calculated automatically if not provided
        self.__total_amount = total_amount if total_amount is not None else (consultation_fee + medicine_cost + labtest_cost)

    # Getters
    def get_bill_id(self): return self.__bill_id
    def get_patient_id(self): return self.__patient_id
    def get_appointment_id(self): return self.__appointment_id
    def get_medicine_prescription_id(self): return self.__medicine_prescription_id
    def get_labtest_prescription_id(self): return self.__labtest_prescription_id
    def get_consultation_fee(self): return self.__consultation_fee
    def get_medicine_cost(self): return self.__medicine_cost
    def get_labtest_cost(self): return self.__labtest_cost
    def get_total_amount(self): return self.__total_amount

    # Setters
    def set_consultation_fee(self, consultation_fee): 
        self.__consultation_fee = consultation_fee
        self.__calculate_total()
    def set_medicine_cost(self, medicine_cost): 
        self.__medicine_cost = medicine_cost
        self.__calculate_total()
    def set_labtest_cost(self, labtest_cost): 
        self.__labtest_cost = labtest_cost
        self.__calculate_total()
    def set_total_amount(self, total_amount): self.__total_amount = total_amount

    def __calculate_total(self):
        """Automatically calculate total amount"""
        self.__total_amount = self.__consultation_fee + self.__medicine_cost + self.__labtest_cost

    def __str__(self):
        return (f"BillID: {self.__bill_id}, PatientID: {self.__patient_id}, AppointmentID: {self.__appointment_id}, "
                f"MedicinePrescriptionID: {self.__medicine_prescription_id}, LabTestPrescriptionID: {self.__labtest_prescription_id}, "
                f"ConsultationFee: {self.__consultation_fee}, MedicineCost: {self.__medicine_cost}, "
                f"LabTestCost: {self.__labtest_cost}, TotalAmount: {self.__total_amount}")
