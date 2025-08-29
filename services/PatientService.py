from dao.PatientDaoImpl import PatientDaoImpl
from models.Patient import Patient
from lib.PatientManagementLib import PatientManagementLib

class PatientMenu:
    @staticmethod
    def show_menu():
        """Patient Management submenu"""
        while True:
            print("\n" + "="*50)
            print("           PATIENT MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Add Patient")
            print("2. List Patients")
            print("3. Active/Inactive Patient Management")
            print("4. Update Patient")
            print("0. Return to Main Menu")
            print("-"*50)
            
            choice = input("Enter your choice (0-4): ").strip()
            
            if choice == '1':
                PatientService.add_patient()
            elif choice == '2':
                PatientService.list_patients()
            elif choice == '3':
                PatientService.manage_patient_status()
            elif choice == '4':
                PatientService.update_patient()
            elif choice == '0':
                print("Returning to main menu...")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 0 and 4.")

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
    def list_patients(include_inactive=False):
        try:
            patients = PatientService.dao.list_patients(include_inactive=include_inactive)
            if not patients:
                print("No patients found." if not include_inactive else "No patients found (including inactive).")
                return
            print("\n--- " + ("All Patients (Including Inactive)" if include_inactive else "Active Patients") + " ---")
            for p in patients:
                status = " (Inactive)" if not p.get_isactive() else ""
                print(f"{p}{status}")
        except Exception as e:
            print(f"Error listing patients: {e}")

    @staticmethod
    def delete_patient():
        try:
            # First list all active patients to show available IDs
            patients = PatientService.dao.list_patients(include_inactive=False)
            if not patients:
                print("No active patients found to deactivate.")
                return
            
            print("\n--- Active Patients ---")
            for p in patients:
                print(p)
            
            # Get patient ID to deactivate
            while True:
                try:
                    patient_id = int(input("\nEnter patient ID to deactivate: "))
                    if patient_id > 0:
                        # Verify patient exists and is active
                        patient = next((p for p in patients if p.get_patientid() == patient_id), None)
                        if patient:
                            break
                        print(f"Error: No active patient found with ID {patient_id}.")
                    else:
                        print("Error: Patient ID must be a positive integer.")
                except ValueError:
                    print("Error: Please enter a valid integer for patient ID.")
            
            # Confirm deactivation
            confirm = input(f"Are you sure you want to deactivate patient ID {patient_id}? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Deactivation cancelled.")
                return
            
            # Deactivate the patient (soft delete)
            success = PatientService.dao.delete_patient(patient_id)
            if success:
                print(f"Patient with ID {patient_id} has been deactivated successfully.")
            else:
                print(f"Failed to deactivate patient with ID {patient_id}. Patient may not exist or is already inactive.")
                
        except Exception as e:
            print(f"Error deactivating patient: {e}")

    @staticmethod
    def manage_patient_status():
        """Menu to list all patients and toggle their active status"""
        try:
            while True:
                print("\n--- Patient Management ---")
                print("1. List active patients")
                print("2. List all patients (including inactive)")
                print("3. Toggle patient status (active/inactive)")
                print("4. Back to main menu")
                
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == '1':
                    # List only active patients
                    patients = PatientService.dao.list_patients(include_inactive=False)
                    if not patients:
                        print("No active patients found in the system.")
                        continue
                        
                    print("\n--- Active Patients ---")
                    for p in patients:
                        print(f"ID: {p.get_patientid()}, Name: {p.get_name()}, "
                              f"Mobile: {p.get_mobileno()}, DOB: {p.get_dob()}")
                
                elif choice == '2':
                    # List all patients including inactive ones
                    patients = PatientService.dao.list_patients(include_inactive=True)
                    if not patients:
                        print("No patients found in the system.")
                        continue
                        
                    print("\n--- All Patients (Including Inactive) ---")
                    for p in patients:
                        status = "Active" if p.get_isactive() else "Inactive"
                        print(f"ID: {p.get_patientid()}, Name: {p.get_name()}, Status: {status}, "
                              f"Mobile: {p.get_mobileno()}, DOB: {p.get_dob()}")
                
                elif choice == '3':
                    # Toggle patient status
                    patients = PatientService.dao.list_patients(include_inactive=True)
                    if not patients:
                        print("No patients found in the system.")
                        continue
                        
                    # Show all patients with their status
                    print("\n--- All Patients ---")
                    for p in patients:
                        status = "Active" if p.get_isactive() else "Inactive"
                        print(f"ID: {p.get_patientid()}, Name: {p.get_name()}, Status: {status}")
                    
                    # Get patient ID to toggle
                    try:
                        patient_id = int(input("\nEnter patient ID to toggle status (or 0 to cancel): ").strip())
                        if patient_id == 0:
                            print("Operation cancelled.")
                            continue
                            
                        patient = next((p for p in patients if p.get_patientid() == patient_id), None)
                        if not patient:
                            print(f"Error: No patient found with ID {patient_id}")
                            continue
                            
                        new_status = not patient.get_isactive()
                        status_text = "activate" if new_status else "deactivate"
                        
                        confirm = input(f"Are you sure you want to {status_text} patient ID {patient_id}? (y/n): ").strip().lower()
                        if confirm != 'y':
                            print("Operation cancelled.")
                            continue
                            
                        # Update the status in the database
                        success = PatientService.dao.update_patient_status(patient_id, new_status)
                        if success:
                            status_text = "activated" if new_status else "deactivated"
                            print(f"Patient ID {patient_id} has been {status_text} successfully.")
                        else:
                            print(f"Failed to update status for patient ID {patient_id}.")
                            
                    except ValueError:
                        print("Error: Please enter a valid patient ID.")
                
                elif choice == '4':
                    print("Returning to main menu...")
                    break
                    
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
                    
        except Exception as e:
            print(f"Error in patient management: {e}")
            import traceback
            traceback.print_exc()

    @staticmethod
    def update_patient():
        try:
            # First list all patients to show available IDs
            patients = PatientService.dao.list_patients()
            if not patients:
                print("No patients found to update.")
                return
            
            print("\n--- Available Patients ---")
            for p in patients:
                print(p)
            
            # Get patient ID to update
            while True:
                try:
                    patient_id = int(input("\nEnter patient ID to update: "))
                    if patient_id > 0:
                        break
                    print("Error: Patient ID must be a positive integer.")
                except ValueError:
                    print("Error: Please enter a valid integer for patient ID.")
            
            # Get the existing patient
            existing_patient = PatientService.dao.get_patient_by_id(patient_id)
            if not existing_patient:
                print(f"Patient with ID {patient_id} not found.")
                return
            
            print(f"\nCurrent patient details: {existing_patient}")
            print("\nEnter new values (press Enter to keep current value):")
            
            # Get and validate name
            while True:
                name = input(f"Enter patient name [{existing_patient.get_name()}]: ").strip()
                if not name:  # Keep current value
                    name = existing_patient.get_name()
                    break
                if PatientManagementLib.validate_name(name):
                    break
                print("Error: Invalid name! Name must be at least 3 characters long and contain only letters, spaces, and hyphens.")
                print("Please try again.\n")

            # Get and validate DOB
            while True:
                dob = input(f"Enter DOB (YYYY-MM-DD) [{existing_patient.get_dob()}]: ").strip()
                if not dob:  # Keep current value
                    dob = existing_patient.get_dob()
                    break
                if PatientManagementLib.validate_dob(dob):
                    break
                print("Error: Invalid date of birth! Please use YYYY-MM-DD format and ensure the date is not in the future.")
                print("Please try again.\n")

            # Get and validate gender
            while True:
                gender = input(f"Enter Gender (Male/Female/Other) [{existing_patient.get_gender()}]: ").strip()
                if not gender:  # Keep current value
                    gender = existing_patient.get_gender()
                    break
                if PatientManagementLib.validate_gender(gender):
                    break
                print("Error: Invalid gender! Please enter Male, Female, or Other (M/F/O).")
                print("Please try again.\n")

            # Get and validate blood group
            while True:
                bloodgroup = input(f"Enter Blood Group (A+/A-/B+/B-/AB+/AB-/O+/O-) [{existing_patient.get_bloodgroup()}]: ").strip()
                if not bloodgroup:  # Keep current value
                    bloodgroup = existing_patient.get_bloodgroup()
                    break
                if PatientManagementLib.validate_bloodgroup(bloodgroup):
                    break
                print("Error: Invalid blood group! Allowed: A+/A-/B+/B-/AB+/AB-/O+/O-.")
                print("Please try again.\n")

            # Get and validate mobile
            while True:
                mobile = input(f"Enter Mobile (10 digits starting with 6/7/8/9) [{existing_patient.get_mobileno()}]: ").strip()
                if not mobile:  # Keep current value
                    mobile = existing_patient.get_mobileno()
                    break
                if PatientManagementLib.validate_mobile(mobile):
                    break
                print("Error: Invalid mobile number! Must be 10 digits and start with 6/7/8/9.")
                print("Please try again.\n")

            # Get and validate address
            while True:
                address = input(f"Enter Address [{existing_patient.get_address()}]: ").strip()
                if not address:  # Keep current value
                    address = existing_patient.get_address()
                    break
                if PatientManagementLib.validate_address(address):
                    break
                print("Error: Invalid address! Address must be between 5 and 200 characters long.")
                print("Please try again.\n")

            # Create updated patient object
            updated_patient = Patient(patient_id, name, dob, gender, bloodgroup, mobile, address, existing_patient.get_isactive())
            
            # Confirm update
            print(f"\nUpdated patient details: {updated_patient}")
            confirm = input("Are you sure you want to update this patient? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Update cancelled.")
                return
            
            # Update the patient
            success = PatientService.dao.update_patient(updated_patient)
            if success:
                print(f"Patient with ID {patient_id} updated successfully.")
            else:
                print(f"Failed to update patient with ID {patient_id}.")
                
        except Exception as e:
            print(f"Error updating patient: {e}")
