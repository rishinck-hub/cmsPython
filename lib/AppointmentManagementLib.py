from datetime import datetime

class AppointmentManagementLib:
    @staticmethod
    def validate_status(status):
        """Validate appointment status (pending, cancelled, completed)"""
        if not status or not isinstance(status, str):
            return False
        valid_statuses = ["pending", "cancelled", "completed"]
        return status.lower() in valid_statuses

    @staticmethod
    def validate_date(date):
        """Validate appointment date - must be today or in the future"""
        if not date or not isinstance(date, str):
            return False
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            current_date = datetime.now().date()
            
            # Appointment date should be today or in the future
            return date_obj.date() >= current_date
        except ValueError:
            return False

    @staticmethod
    def validate_token_no(token_no):
        """Validate token number - positive integer"""
        try:
            token_int = int(token_no)
            return token_int > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_appointment_id(appointment_id):
        """Validate appointment ID - positive integer"""
        try:
            appointment_id_int = int(appointment_id)
            return appointment_id_int > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_patient_id(patient_id):
        """Validate patient ID - positive integer"""
        try:
            patient_id_int = int(patient_id)
            return patient_id_int > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_doctor_id(doctor_id):
        """Validate doctor ID - positive integer"""
        try:
            doctor_id_int = int(doctor_id)
            return doctor_id_int > 0
        except (ValueError, TypeError):
            return False
