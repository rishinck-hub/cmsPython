from datetime import date
import re

class ConsultationValidation:

    @staticmethod
    def validate_consultation_id(consultation_id):
        if consultation_id is None or not isinstance(consultation_id, int) or consultation_id <= 0:
            raise ValueError("Consultation ID must be a positive integer.")

    @staticmethod
    def validate_symptoms(symptoms):
        if not symptoms or not isinstance(symptoms, str):
            raise ValueError("Symptoms must be a non-empty string.")

    @staticmethod
    def validate_diagnosis(diagnosis):
        if not diagnosis or not isinstance(diagnosis, str):
            raise ValueError("Diagnosis must be a non-empty string.")

    @staticmethod
    def validate_created_date(created_date):
        if created_date is None:
            raise ValueError("Created date cannot be None.")
        if not isinstance(created_date, date):
            raise ValueError("Created date must be a valid date object.")
        if created_date > date.today():
            raise ValueError("Created date cannot be in the future.")

    @staticmethod
    def validate_appointment_id(appointment_id):
        if appointment_id is None or not isinstance(appointment_id, int) or appointment_id <= 0:
            raise ValueError("Appointment ID must be a positive integer.")
    @staticmethod
    def validate_medicine_id(medicine_id: int) -> bool:
        """Validate medicine ID: must be a positive integer."""
        return isinstance(medicine_id, int) and medicine_id > 0

    @staticmethod
    def validate_dosage(dosage: str) -> bool:
        """Validate dosage: non-empty string (e.g., '500mg', '2 tablets')."""
        return isinstance(dosage, str) and len(dosage.strip()) > 0

    @staticmethod
    def validate_frequency(frequency: str) -> bool:
        """Validate frequency: must be a non-empty string (e.g., '2 times a day')."""
        return isinstance(frequency, str) and len(frequency.strip()) > 0

    @staticmethod
    def validate_duration(duration: str) -> bool:
        """Validate duration: must be non-empty (e.g., '5 days')."""
        return isinstance(duration, str) and len(duration.strip()) > 0

    @staticmethod
    def validate_quantity(quantity: int) -> bool:
        """Validate quantity: must be positive integer."""
        return isinstance(quantity, int) and quantity > 0

    @staticmethod
    def validate_appointment_id(appointment_id: int) -> bool:
        """Validate appointment ID: must be positive integer."""
        return isinstance(appointment_id, int) and appointment_id > 0


class LabTestPrescriptionValidation:
    @staticmethod
    def validate_labtest_id(labtest_id: int) -> bool:
        return isinstance(labtest_id, int) and labtest_id > 0

    @staticmethod
    def validate_created_date(created_date) -> bool:
        return isinstance(created_date, date) and created_date <= date.today()

    @staticmethod
    def validate_remarks(remarks: str) -> bool:
        return isinstance(remarks, str) and len(remarks.strip()) > 0 and len(remarks) <= 200

    @staticmethod
    def validate_appointment_id(appointment_id: int) -> bool:
        return isinstance(appointment_id, int) and appointment_id > 0
