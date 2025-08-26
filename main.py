from services.PatientService import PatientService
from services.AppointmentService import AppointmentService

def validate_menu_choice(choice):
    """Validate menu choice input"""
    try:
        choice_int = int(choice)
        return 0 <= choice_int <= 4
    except ValueError:
        return False

def menu():
    while True:
        print("\n" + "="*50)
        print("           RECEPTIONIST MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Patient")
        print("2. List Patients")
        print("3. Book Appointment")
        print("4. List Appointments")
        print("0. Exit")
        print("-"*50)

        # Loop until valid choice is entered
        while True:
            choice = input("Enter your choice (0-4): ").strip()
            
            if validate_menu_choice(choice):
                choice_int = int(choice)
                break
            else:
                print("Error: Please enter a valid number between 0 and 4!")
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
            AppointmentService.book_appointment()
        elif choice_int == 4:
            AppointmentService.list_appointments()
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the application.")
