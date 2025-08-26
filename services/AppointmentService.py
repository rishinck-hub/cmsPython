from dao.AppointmentDaoImpl import AppointmentDaoImpl
from models.Appointment import Appointment
from lib.AppointmentManagementLib import AppointmentManagementLib
from db.db_connection import DBConnection

class AppointmentService:
    dao = AppointmentDaoImpl()
    appointment_counter = 1

    @staticmethod
    def _record_exists(table_name: str, id_column: str, id_value: int) -> bool:
        """Check if a record exists in the given table by id."""
        conn = DBConnection().get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            query = f"SELECT 1 FROM {table_name} WHERE {id_column}=%s LIMIT 1"
            cursor.execute(query, (id_value,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error validating {table_name} id:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def _get_booked_tokens(date_str: str, doctor_id: int):
        """Return a sorted list of already booked token numbers for a doctor on a given date."""
        conn = DBConnection().get_connection()
        cursor = None
        tokens = []
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tokenno FROM appointments WHERE `date`=%s AND doctorid=%s",
                (date_str, doctor_id),
            )
            tokens = sorted([int(r[0]) for r in cursor.fetchall() if r and r[0] is not None])
        except Exception as e:
            print("Error fetching booked tokens:", e)
        finally:
            if cursor:
                cursor.close()
        return tokens

    @staticmethod
    def book_appointment():
        try:
            # Get and validate date
            while True:
                date = input("Enter appointment date (YYYY-MM-DD): ").strip()
                if AppointmentManagementLib.validate_date(date):
                    break
                print("Error: Invalid appointment date! Date must be today or in the future.")
                print("Please try again.\n")

            # Get and validate status
            while True:
                status = input("Enter status (Pending/Cancelled/Completed): ").strip()
                if AppointmentManagementLib.validate_status(status):
                    break
                print("Error: Invalid status! Please enter Pending, Cancelled, or Completed.")
                print("Please try again.\n")

            # Get and validate patient ID and existence
            while True:
                patient_id_input = input("Enter Patient ID: ").strip()
                if AppointmentManagementLib.validate_patient_id(patient_id_input):
                    patient_id = int(patient_id_input)
                    if AppointmentService._record_exists("patients", "patientid", patient_id):
                        break
                    print("Error: Patient ID does not exist. Please enter a valid Patient ID.")
                else:
                    print("Error: Invalid patient ID! Please enter a positive integer.")
                print("Please try again.\n")

            # Get and validate doctor ID and existence
            while True:
                doctor_id_input = input("Enter Doctor ID: ").strip()
                if AppointmentManagementLib.validate_doctor_id(doctor_id_input):
                    doctor_id = int(doctor_id_input)
                    if AppointmentService._record_exists("doctors", "doctorid", doctor_id):
                        break
                    print("Error: Doctor ID does not exist. Please enter a valid Doctor ID.")
                else:
                    print("Error: Invalid doctor ID! Please enter a positive integer.")
                print("Please try again.\n")

            # Enforce token limit per doctor per date and show booked tokens
            booked_tokens = AppointmentService._get_booked_tokens(date, doctor_id)
            print("\nBooked tokens for this doctor on", date, ":", (booked_tokens if booked_tokens else "None"))
            if len(booked_tokens) >= 25:
                print("Error: This doctor already has 25 tokens booked for", date, "Please choose another date or doctor.")
                return

            # Show available tokens before asking for input
            available_tokens = [i for i in range(1, 26) if i not in booked_tokens]
            print("Available tokens:", available_tokens if available_tokens else "None")

            # Get and validate token number with availability and bounds 1..25
            while True:
                token_input = input("Enter token no (1-25 and not already booked): ").strip()
                if AppointmentManagementLib.validate_token_no(token_input):
                    token = int(token_input)
                    if 1 <= token <= 25 and token not in booked_tokens:
                        break
                    if token in booked_tokens:
                        print("Error: Token number already booked. Choose another token.")
                    else:
                        print("Error: Token number must be between 1 and 25.")
                else:
                    print("Error: Invalid token number! Please enter a positive integer.")
                print("Please try again.\n")

            # Create appointment object (validation happens in constructor)
            appointment = Appointment(AppointmentService.appointment_counter, date, token, status, patient_id, doctor_id)
            AppointmentService.dao.book_appointment(appointment)
            print("Appointment booked successfully with ID:", AppointmentService.appointment_counter)
            AppointmentService.appointment_counter += 1
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def list_appointments():
        try:
            appointments = AppointmentService.dao.list_appointments()
            if not appointments:
                print("No appointments found.")
                return
            print("\n--- Appointment List ---")
            for a in appointments:
                print(a)
        except Exception as e:
            print(f"Error listing appointments: {e}")
