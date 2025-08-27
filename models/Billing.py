# models/bill.py

from datetime import datetime

class Bill:
    """
    A class representing a billing record including medicine billing and related details.
    """

    def __init__(
        self,
        billingid=None,
        patientid=None,
        appointmentid=None,
        medicineprescriptionid=None,
        labtestprescriptionid=None,
        consultationfee=0.0,
        medicineamount=0.0,
        labtestamount=0.0,
        totalamount=0.0
    ):
        self._billingid = billingid
        self._patientid = patientid
        self._appointmentid = appointmentid
        self._medicineprescriptionid = medicineprescriptionid
        self._labtestprescriptionid = labtestprescriptionid
        self.consultationfee = consultationfee
        self.medicineamount = medicineamount
        self.labtestamount = labtestamount
        self._date = datetime.now()

    # billingid property
    @property
    def billingid(self):
        return self._billingid

    @billingid.setter
    def billingid(self, value):
        self._billingid = value

    # patientid property
    @property
    def patientid(self):
        return self._patientid

    @patientid.setter
    def patientid(self, value):
        self._patientid = value

    # appointmentid property
    @property
    def appointmentid(self):
        return self._appointmentid

    @appointmentid.setter
    def appointmentid(self, value):
        self._appointmentid = value

    # consultationfee property
    @property
    def consultationfee(self):
        return self._consultationfee

    @consultationfee.setter
    def consultationfee(self, value):
        if value is not None and value < 0:
            raise ValueError("Consultation fee cannot be negative.")
        self._consultationfee = float(value or 0.0)

    # medicineamount property
    @property
    def medicineamount(self):
        return self._medicineamount

    @medicineamount.setter
    def medicineamount(self, value):
        if value is not None and value < 0:
            raise ValueError("Medicine amount cannot be negative.")
        self._medicineamount = float(value or 0.0)

    # labtestamount property
    @property
    def labtestamount(self):
        return self._labtestamount

    @labtestamount.setter
    def labtestamount(self, value):
        if value is not None and value < 0:
            raise ValueError("Lab test amount cannot be negative.")
        self._labtestamount = float(value or 0.0)

    # totalamount property (computed, read-only)
    @property
    def totalamount(self):
        return (
            (self.consultationfee or 0.0) +
            (self.medicineamount or 0.0) +
            (self.labtestamount or 0.0)
        )

    # date property (read-only)
    @property
    def date(self):
        return self._date

    def __str__(self):
        return (
            f"Bill ID: {self.billingid} | "
            f"Patient ID: {self.patientid} | "
            f"Appointment ID: {self.appointmentid} | "
            f"Date: {self.date.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"Consultation Fee: {self.consultationfee:.2f} | "
            f"Medicine Amount: {self.medicineamount:.2f} | "
            f"Lab Test Amount: {self.labtestamount:.2f} | "
            f"Total Amount: {self.totalamount:.2f}"
        )
