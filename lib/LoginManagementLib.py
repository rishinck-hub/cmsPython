from services.Auth_service import AuthService
from lib.staffManagementLib import StaffManagementLib
from lib.DoctorManagementLib import DoctorManagementLib
from lib.DoctorManagementLib import MedicinePrescriptionManagementLib
from lib.DoctorManagementLib import ConsultationManagementLib

from lib.DoctorManagementLib import LabTestPrescriptionManagementLib
# from lib.AppointmentManagementLib import AppointmentManagementLib
# from lib.LabTestManagementLib import LabTestManagementLib
from lib.MedicineManagementLib import MedicineManagementLib
# from lib.BillingManagementLib import BillingManagementLib
from services.PatientService import PatientService
from services.AppointmentService import AppointmentService

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
            print("\n--- Admin Dashboard ---")
            print("1. display Staffs")
            print('2. add staffs')
            print("3. display Doctors")
            print("4. add doctor")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                StaffManagementLib.display_all()
            elif choice == "2":
                StaffManagementLib.add_staff()
            # elif choice == "3":
                
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice")

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
            print("\n--- Receptionist Dashboard ---")
            print("1. Register Patient")
            print('2.view all patient')
            print("3. Book Appointment")
            print("4. View Appointments")
            print("5. Logout")
            choice = input("Enter choice: ")

            if choice == "1":
                PatientService.add_patient()
            elif choice == "2":
                PatientService.list_patients()
            elif choice == "3":
                AppointmentService.book_appointment()
            elif choice =="4":
                AppointmentService.list_appointments()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice")

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
