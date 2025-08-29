from services.Auth_service import AuthService
from lib.staffManagementLib import StaffManagementLib
from lib.DoctorManagementLib import DoctorManagementLib
from lib.DoctorManagementLib import MedicinePrescriptionManagementLib
from lib.DoctorManagementLib import ConsultationManagementLib
from lib.staffManagementLib import StaffManagementLib, DoctorManageLib
from lib.DoctorManagementLib import LabTestPrescriptionManagementLib
# from lib.AppointmentManagementLib import AppointmentManagementLib
# from lib.LabTestManagementLib import LabTestManagementLib
from lib.MedicineManagementLib import MedicineManagementLib
# from lib.BillingManagementLib import BillingManagementLib
from services.PatientService import PatientService
from services.AppointmentService import AppointmentService
from services.PatientService import PatientMenu
from services.AppointmentService import AppointmentMenu
from services.BillingService import BillMenu
from models.Staff import Staff
from models.Doctor import Doctor

class LoginManagementLib:

    @staticmethod
    def login():
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        auth_service = AuthService()
        result = auth_service.login(username, password)

        if result["success"]:
            print(f"\nWelcome {result['fullname']} (RoleID: {result['roleid']})")
            LoginManagementLib.show_dashboard(result)
        else:
            print(f"\nLogin Failed: {result['message']}")

    @staticmethod
    def show_dashboard(user):
        roleid = user["roleid"]
        if roleid == 1:  
            LoginManagementLib.admin_menu()
        elif roleid == 2:  
            LoginManagementLib.doctor_menu()
        elif roleid == 3:  
            LoginManagementLib.receptionist_menu()
        elif roleid == 4:  
            LoginManagementLib.pharmacist_menu()
        elif roleid == 5:  
            LoginManagementLib.pharmacist_menu()
        else:
            print("Unknown Role")

    # ---------------- Menus ---------------- #
    @staticmethod
    def admin_menu():
        while True:
            print("\n============= ADMIN MANAGEMENT MENU ==============")
            print("1. Manage Staff")
            print("2. Manage Doctors")
            print("3. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                LoginManagementLib.staff_management_menu()
            elif choice == "2":
                LoginManagementLib.doctor_management_menu()
            elif choice == "3":
                print(" Logging out...")
                break
            else:
                print(" Invalid choice!")
    @staticmethod
    def staff_management_menu():
        while True:
            print("\n=============STAFF MANAGEMENT MENU==============")
            print("1. ADD STAFF")
            print("2. SEE LIST OF STAFFS")
            print("3. SEARCH AND VIEW STAFF")
            print("4. GO TO MAIN MENU")
            choice = input("Enter your choice:")
            if choice == "1":
                    StaffManagementLib.add_staff()
            elif choice == "2":
                    StaffManagementLib.display_all()
            elif choice == "3":
                    print("\n========= Search Staff Menu =========")
                    print("1. By Staff Number")
                    print("2. By Phone Number")
                    print("3. Go Back")

                    search_choice = input("Enter your choice (1-3): ")

                    staff = None
                    if search_choice == "1":
                        staff = StaffManagementLib.search_by_staffid()
                    elif search_choice == "2":
                        staff = StaffManagementLib.search_by_mobileno()
                    elif search_choice == "3":
                        continue
                    else:
                        print(" Invalid choice! Please enter 1, 2, or 3.")
                        continue

                    if staff:  # staff found
                        print(f"\nStaff Found: {staff.get_fullname()} ({staff.get_mobileno()})")

                    while True:
                        print("\n========= Staff Action Menu =========")
                        print("1. Edit Staff")
                        print("2. Disable Staff")
                        print("3. Go Back")

                        action_choice = input("Enter your choice (1-3): ")
                        if action_choice == "1":
                            LoginManagementLib.edit_staff_menu(staff)
                        elif action_choice == "2":
                            StaffManagementLib.disable_staff(staff)
                            break
                        elif action_choice == "3":
                            break
                        else:  
                            print(" Invalid choice. Try again.")
            elif choice == "4":
                break
            else:
                print(" Invalid choice, try again!")

    @staticmethod
    def edit_staff_menu(staff):
        while True:
            print("\n========= Edit Staff Menu =========")
            print("1. Name")
            print("2. Mobile no")
            print("3. Go Back")

            choice = input("Which field do you want to edit? (1-3): ")

            if choice == "1":
                new_name = input("Enter new Name: ")
                StaffManagementLib.update_staff_name(staff, new_name)

            elif choice == "2":
                new_mobile = input("Enter new Mobile No (10 digits): ")
                StaffManagementLib.update_staff_mobileno(staff, new_mobile)

            elif choice == "3":
                break  

            else:
                print(" Invalid choice. Try again.")

    @staticmethod            
    def doctor_management_menu():
        while True:
            print("\n============= DOCTOR MANAGEMENT MENU ==============")
            print("1. ADD DOCTOR")
            print("2. LIST DOCTORS")
            print("3. SEARCH DOCTOR")
            print("4. DISABLE DOCTOR")
            print("5. GO TO MAIN MENU")

            choice = input("Enter your choice: ")

            if choice == "1":
                DoctorManageLib.add_doctor()

            elif choice == "2":
                DoctorManageLib.list_doctors()

            elif choice == "3":
                DoctorManageLib.search_doctor()
                
            elif choice == "4":
                DoctorManageLib.disable_doctor()

            elif choice == "5":
                break
            else:
                print(" Invalid choice, try again!")



    @staticmethod
    def doctor_menu():
        doctor_id = input('Enter the doctor id : ')
        while True:
            print("\n--- Doctor Dashboard ---")
            print("1. View Appointments")
            print("2. Add Consultation")
            print("3. Prescribe Medicines")
            print("4. Prescribe Lab Tests")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                DoctorManagementLib.view_appointments(doctor_id)
            elif choice == "2":
                appointments = DoctorManagementLib.get_todays_appointments(doctor_id)

                if not appointments:
                    continue
                else:
                    print("These are today's appointments")
                    ConsultationManagementLib.add_consultation()
            elif choice == "3":
                appointments = DoctorManagementLib.get_todays_appointments(doctor_id)

                if not appointments:
                    continue
                else:
                    print("These are today's appointments")
                    MedicinePrescriptionManagementLib.add_prescription()
            elif choice == "4":
                appointments = DoctorManagementLib.get_todays_appointments(doctor_id)

                if not appointments:
                    continue
                else:
                    print("These are today's appointments")
                    LabTestPrescriptionManagementLib.add_prescription()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice")

    @staticmethod
    def receptionist_menu():
            while True:
                print("\n" + "="*50)
                print("           RECEPTIONIST MANAGEMENT SYSTEM")
                print("="*50)
                print("1. Patient Management")
                print("2. Appointment Management")
                print("3. Bill Management")
                print("0. Exit")
                print("-"*50)
                choice = input("Enter your choice (0-3): ").strip()


                # Loop until valid choice is entered
                while True:                    
                # Handle exit first
                    if choice == "0":
                        print("Thank you for using the Receptionist Management System!")
                        print("Goodbye!")
                        return  # Exit the function
                    
                    # Handle management sections
                    if choice == "1":
                        PatientMenu.show_menu()
                        break
                    elif choice == "2":
                        AppointmentMenu.show_menu()
                        break
                    elif choice == "3":
                        BillMenu.show_menu()
                        break
                    else:
                        print("Invalid choice. Please try again.")
                        break


        
    @staticmethod
    def labtech_menu():
        while True:
            print("\n--- Lab Technician Dashboard ---")
            print("1. View Lab Prescriptions")
            print("2. Enter Test Results")
            print("3. Logout")
            choice = input("Enter choice: ")

            # if choice == "1":
            #     LabTestManagementLib.view_prescriptions()
            # elif choice == "2":
            #     LabTestManagementLib.add_result()
            # elif choice == "3":
            #     print("Logging out...")
            #     break
            # else:
            #     print("Invalid choice")

    @staticmethod
    def pharmacist_menu():
        while True:
            print("\n--- Pharmacist Dashboard ---")
            print("1. Add medicines")
            print("2. Display all")
            print("3. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                MedicineManagementLib.add_medicine()
            elif choice == "2":
                MedicineManagementLib.display_all()
            elif choice == "3":
                print("Logging out...")
                break
            else:
                print("Invalid choice")
