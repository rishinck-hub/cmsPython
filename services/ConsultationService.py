from datetime import date

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
