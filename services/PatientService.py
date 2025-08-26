from dao.PatientDaoImpl import PatientDaoImpl
from models.Patient import Patient
from lib.PatientManagementLib import PatientManagementLib

class PatientService:
    dao = PatientDaoImpl()
    patient_counter = 1

    @staticmethod
    def add_patient():
        try:
            # Get and validate name
            while True:
                name = input("Enter patient name: ").strip()
                if PatientManagementLib.validate_name(name):
                    break
                print("Error: Invalid name! Name must be at least 3 characters long and contain only letters, spaces, and hyphens.")
                print("Please try again.\n")

            # Get and validate DOB
            while True:
                dob = input("Enter DOB (YYYY-MM-DD): ").strip()
                if PatientManagementLib.validate_dob(dob):
                    break
                print("Error: Invalid date of birth! Please use YYYY-MM-DD format and ensure the date is not in the future.")
                print("Please try again.\n")

            # Get and validate gender
            while True:
                gender = input("Enter Gender (Male/Female/Other): ").strip()
                if PatientManagementLib.validate_gender(gender):
                    break
                print("Error: Invalid gender! Please enter Male, Female, or Other (M/F/O).")
                print("Please try again.\n")

            # Get and validate blood group
            while True:
                bloodgroup = input("Enter Blood Group (A+/A-/B+/B-/AB+/AB-/O+/O-): ").strip()
                if PatientManagementLib.validate_bloodgroup(bloodgroup):
                    break
                print("Error: Invalid blood group! Allowed: A+/A-/B+/B-/AB+/AB-/O+/O-.")
                print("Please try again.\n")

            # Get and validate mobile
            while True:
                mobile = input("Enter Mobile (10 digits starting with 6/7/8/9): ").strip()
                if PatientManagementLib.validate_mobile(mobile):
                    break
                print("Error: Invalid mobile number! Must be 10 digits and start with 6/7/8/9.")
                print("Please try again.\n")

            # Get and validate address
            while True:
                address = input("Enter Address: ").strip()
                if PatientManagementLib.validate_address(address):
                    break
                print("Error: Invalid address! Address must be between 5 and 200 characters long.")
                print("Please try again.\n")

            # Create patient object without ID (auto-increment in DB)
            patient = Patient(None, name, dob, gender, bloodgroup, mobile, address)
            ok, new_id = PatientService.dao.add_patient(patient)
            if ok:
                print("Patient added successfully with ID:", new_id)
            else:
                print("Failed to add patient.")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def list_patients():
        try:
            patients = PatientService.dao.list_patients()
            if not patients:
                print("No patients found.")
                return
            print("\n--- Patient List ---")
            for p in patients:
                print(p)
        except Exception as e:
            print(f"Error listing patients: {e}")
