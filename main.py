from services.PatientService import PatientService
from services.AppointmentService import AppointmentService

def validate_menu_choice(choice):
    """Validate menu choice input"""
    try:
        choice_int = int(choice)
        return 0 <= choice_int <= 9  # Updated range to include cancel appointment
    except ValueError:
        return False

def wait_for_main_menu():
    input("\nPress Enter to return to the main menu...")

def menu():
    while True:
        print("\n" + "="*50)
        print("           RECEPTIONIST MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add New Patient")
        print("2. List Patients")
        print("3. Patient Management (Active/Inactive)")
        print("4. Update Patient Details")
        print("5. Book Appointment")
        print("6. List Appointments")
        print("7. Update Appointment")
        print("8. Cancel Appointment")
        print("0. Exit")
        print("-"*50)

        # Loop until valid choice is entered
        while True:
            choice = input("Enter your choice (0-7): ").strip()
            
            if validate_menu_choice(choice):
                choice_int = int(choice)
                if 0 <= choice_int <= 8:  # Updated range to include list patients
                    break
                print("Error: Please enter a valid number between 0 and 8!")
            else:
                print("Error: Please enter a valid number!")
            print("Please try again.\n")
        
        # Handle exit first
        if choice_int == 0:
            print("Thank you for using the Receptionist Management System!")
            print("Goodbye!")
            return  # Exit the function
        
        # Handle other menu options
        elif choice_int == 1:
            PatientService.add_patient()
        elif choice_int == 2:
            PatientService.list_patients()
        elif choice_int == 3:
            PatientService.manage_patient_status()
        elif choice_int == 4:
            PatientService.update_patient()
        elif choice_int == 5:
            AppointmentService.book_appointment()
        elif choice_int == 6:
            AppointmentService.list_appointments()
        elif choice_int == 7:
            AppointmentService.update_appointment()
        elif choice_int == 8:
            AppointmentService.cancel_appointment()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the application.")
