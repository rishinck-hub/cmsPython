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
    def _get_doctor_fee(doctor_id: int):
        """Fetch the consultation fee for a doctor from the doctors table."""
        conn = DBConnection().get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT consultationfee FROM doctors WHERE doctorid=%s", (doctor_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            fee = row[0]
            try:
                return float(fee) if fee is not None else None
            except Exception:
                return None
        except Exception as e:
            print("Error fetching doctor fee:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def _print_booking_receipt(appointment_id: int, patient_id: int, doctor_id: int, date: str, token: int, fee: float):
        line = "-" * 50
        print("\n" + line)
        print("             APPOINTMENT RECEIPT")
        print(line)
        print(f"Appointment ID : {appointment_id}")
        print(f"Patient ID     : {patient_id}")
        print(f"Doctor ID      : {doctor_id}")
        print(f"Date           : {date}")
        print(f"Token Number   : {token}")
        print(f"Consultation Fee: {fee}")
        print(line + "\n")

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

            # Get and validate patient ID, existence, and active status
            while True:
                patient_id_input = input("Enter Patient ID: ").strip()
                if not AppointmentManagementLib.validate_patient_id(patient_id_input):
                    print("Error: Invalid patient ID! Please enter a positive integer.")
                    print("Please try again.\n")
                    continue
                    
                patient_id = int(patient_id_input)
                
                # Check if patient exists and is active
                conn = DBConnection().get_connection()
                cursor = None
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT isactive FROM patients WHERE patientid = %s",
                        (patient_id,)
                    )
                    result = cursor.fetchone()
                    
                    if result is None:
                        print("Error: Patient ID does not exist. Please enter a valid Patient ID.")
                        print("Please try again.\n")
                        continue
                        
                    is_active = result[0] == 'y' or result[0] is True
                    if not is_active:
                        print("Error: This patient is currently inactive and cannot book appointments.")
                        print("Please activate the patient first using the Patient Management menu.")
                        print("Please try again or select a different patient.\n")
                        continue
                        
                    break  # Valid active patient
                        
                except Exception as e:
                    print(f"Error checking patient status: {e}")
                    print("Please try again.\n")
                finally:
                    if cursor:
                        cursor.close()

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

            # Fetch and show consultation fee (no bill table)
            fee = AppointmentService._get_doctor_fee(doctor_id)
            if fee is None:
                print("Error: Could not find consultation fee for this doctor.")
                return
            print(f"\nConsultation Fee for Doctor {doctor_id}: {fee}")
            proceed = input("Proceed with booking? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Booking cancelled.")
                return

            # Enforce token limit per doctor per date and show booked tokens
            print(f"\n[Debug] Booking context → date={date}, doctor_id={doctor_id}")
            booked_tokens = AppointmentService._get_booked_tokens(date, doctor_id)
            print("\nBooked tokens for this doctor on", date, ":", (booked_tokens if booked_tokens else "None"))
            if len(booked_tokens) >= 25:
                print("Error: This doctor already has 25 tokens booked for", date, "Please choose another date or doctor.")
                return

            # Auto-assign the smallest available token between 1 and 25
            available_tokens = [i for i in range(1, 26) if i not in booked_tokens]
            print(f"[Debug] Available tokens: {available_tokens}")
            if not available_tokens:
                print("Error: No tokens available for this doctor on the selected date.")
                return
            token = available_tokens[0]
            print(f"Assigned Token: {token}")

            # Create appointment object and save
            appointment = Appointment(None, date, token, status, patient_id, doctor_id)

            print("\n--- Creating Appointment ---")
            appointment_id = AppointmentService.dao.book_appointment(appointment)
            
            if appointment_id:
                print(f"Appointment booked successfully with ID: {appointment_id}")
                print(f"Token {token} assigned to the patient.")
                # Ask for payment confirmation before printing receipt
                paid = input("Has the consultation fee been received? (y/n): ").strip().lower()
                if paid == 'y':
                    AppointmentService._print_booking_receipt(appointment_id, patient_id, doctor_id, date, token, fee)
                else:
                    print("Payment not received yet. Receipt will not be printed.")
            else:
                print("Failed to book appointment. Please try again.")
                return

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def update_appointment():
        try:
            # First list all appointments to show available IDs
            appointments = AppointmentService.dao.list_appointments()
            if not appointments:
                print("No appointments found to update.")
                return
            
            print("\n--- Available Appointments ---")
            for apt in appointments:
                print(f"ID: {apt.get_appointmentid()}, Date: {apt.get_date()}, "
                      f"Token: {apt.get_tokenno()}, Status: {apt.get_status()}, "
                      f"Patient ID: {apt.get_patientid()}, Doctor ID: {apt.get_doctorid()}")
            
            # Get appointment ID to update
            while True:
                try:
                    apt_id = int(input("\nEnter appointment ID to update: "))
                    appointment = next((a for a in appointments if a.get_appointmentid() == apt_id), None)
                    if appointment:
                        break
                    print(f"Error: No appointment found with ID {apt_id}")
                except ValueError:
                    print("Error: Please enter a valid appointment ID.")
            
            # Get updated appointment details
            print("\nEnter new details (press Enter to keep current value):")
            
            # Get and validate date
            while True:
                new_date = input(f"Date [{appointment.get_date()}]: ").strip()
                if not new_date or AppointmentManagementLib.validate_date(new_date):
                    if new_date:
                        appointment.set_date(new_date)
                    break
                print("Error: Invalid date format. Please use YYYY-MM-DD.")
                print("Please try again.\n")

            # Get and validate patient ID and existence
            while True:
                patient_id_input = input(f"Patient ID [{appointment.get_patientid()}]: ").strip()
                if not patient_id_input:  # Keep current value
                    break
                if AppointmentManagementLib.validate_patient_id(patient_id_input):
                    appointment.set_patientid(int(patient_id_input))
                    if AppointmentService._record_exists("patients", "patientid", appointment.get_patientid()):
                        break
                    print("Error: Patient ID does not exist. Please enter a valid Patient ID.")
                else:
                    print("Error: Invalid patient ID! Please enter a positive integer.")
                print("Please try again.\n")

            # Get and validate doctor ID and existence
            while True:
                doctor_id_input = input(f"Doctor ID [{appointment.get_doctorid()}]: ").strip()
                if not doctor_id_input:  # Keep current value
                    break
                if AppointmentManagementLib.validate_doctor_id(doctor_id_input):
                    appointment.set_doctorid(int(doctor_id_input))
                    if AppointmentService._record_exists("doctors", "doctorid", appointment.get_doctorid()):
                        break
                    print("Error: Doctor ID does not exist. Please enter a valid Doctor ID.")
                else:
                    print("Error: Invalid doctor ID! Please enter a positive integer.")
                print("Please try again.\n")

            # Get and validate status
            while True:
                status_input = input(f"Status [{appointment.get_status()}]: ").strip()
                if not status_input:  # Keep current value
                    break
                if AppointmentManagementLib.validate_status(status_input):
                    appointment.set_status(status_input)
                    break
                print("Error: Invalid status! Must be one of: scheduled, completed, cancelled, no-show")
                print("Please try again.\n")

            # Update the appointment in the database
            success = AppointmentService.dao.update_appointment(appointment)
            if success:
                print(f"Appointment with ID {appointment.get_appointmentid()} updated successfully.")
            else:
                print(f"No update for appointment with ID {appointment.get_appointmentid()}.")
                
        except Exception as e:
            print(f"Error updating appointment: {e}")

    @staticmethod
    def list_appointments():
        """List all appointments in the system."""
        try:
            appointments = AppointmentService.dao.list_appointments()
            if not appointments:
                print("No appointments found.")
                return
            print("\n--- Appointment List ---")
            for apt in appointments:
                print(apt)
            return appointments
        except Exception as e:
            print(f"Error listing appointments: {e}")
            return []

    @staticmethod
    def cancel_appointment():
        """Cancel an appointment by ID, regardless of its current status"""
        try:
            # List all appointments
            appointments = AppointmentService.list_appointments()
            if not appointments:
                return
                

            
            # Get appointment ID to cancel
            while True:
                try:
                    apt_id = int(input("\nEnter appointment ID to cancel (or 0 to go back): "))
                    if apt_id == 0:
                        print("Cancellation cancelled.")
                        return
                        
                    # Check if appointment exists (from all appointments, not just scheduled ones)
                    appointment = next((a for a in appointments 
                                      if a.get_appointmentid() == apt_id), None)
                    if appointment:
                        current_status = appointment.get_status()
                        print(f"Current status of appointment {apt_id}: {current_status}")
                        
                        # Check if already cancelled
                        if current_status.lower() == 'cancelled':
                            print("This appointment is already cancelled.")
                            return
                            
                        # Check if completed
                        if current_status.lower() == 'completed':
                            confirm_completed = input("This appointment is marked as completed. Are you sure you want to cancel it? (y/n): ").strip().lower()
                            if confirm_completed != 'y':
                                print("Cancellation cancelled.")
                                return
                            
                        break
                        
                    print(f"Error: No appointment found with ID {apt_id}")
                except ValueError:
                    print("Error: Please enter a valid appointment ID.")
                        
            # Confirm cancellation
            confirm = input(f"Are you sure you want to cancel appointment ID {apt_id}? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancellation cancelled.")
                return
            
            # Update the appointment status to 'cancelled'
            success = AppointmentService.dao.update_appointment_status(apt_id, 'cancelled')
            if success:
                print(f"Appointment ID {apt_id} has been cancelled successfully.")
            else:
                print(f"Failed to cancel appointment ID {apt_id}.")
                
        except Exception as e:
            print(f"Error cancelling appointment: {e}")
            import traceback
            traceback.print_exc()
