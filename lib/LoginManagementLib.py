from services.Auth_service import AuthService
from lib.staffManagementLib import StaffManagementLib
from lib.DoctorManagementLib import ConsultationManagementLib
from lib.DoctorManagementLib import MedicinePrescriptionManagementLib
from lib.DoctorManagementLib import LabTestPrescriptionManagementLib
# from lib.AppointmentManagementLib import AppointmentManagementLib
# from lib.LabTestManagementLib import LabTestManagementLib
# from lib.MedicineManagementLib import MedicineManagementLib
# from lib.BillingManagementLib import BillingManagementLib
# from lib.PatientManagementLib import PatientManagementLib

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
            LoginManagementLib.doctor_menu(user["doctorid"])
        elif roleid == 3:  
            LoginManagementLib.receptionist_menu()
        elif roleid == 4:  
            LoginManagementLib.labtech_menu()
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
    def doctor_menu(doctorid):
        while True:
            print("\n--- Doctor Dashboard ---")
            print("1. View Appointments")
            print("2. Add Consultation")
            print("3. Prescribe Medicines")
            print("4. Prescribe Lab Tests")
            print("5. Logout")
            choice = input("Enter choice: ")

            # if choice == "1":
            #     DoctorManagementLib.view_appointments(doctorid)
            # elif choice == "2":
            #     DoctorManagementLib.add_consultation(doctorid)
            # elif choice == "3":
            #     DoctorManagementLib.prescribe_medicine(doctorid)
            # elif choice == "4":
            #     DoctorManagementLib.prescribe_lab_test(doctorid)
            # elif choice == "5":
            #     print("Logging out...")
            #     break
            # else:
            #     print("Invalid choice")

    @staticmethod
    def receptionist_menu():
        while True:
            print("\n--- Receptionist Dashboard ---")
            print("1. Register Patient")
            print("2. Book Appointment")
            print("3. View Appointments")
            print("4. Logout")
            choice = input("Enter choice: ")

            # if choice == "1":
            #     PatientManagementLib.add_patient()
            # elif choice == "2":
            #     AppointmentManagementLib.add_appointment()
            # elif choice == "3":
            #     AppointmentManagementLib.display_all()
            # elif choice == "4":
            #     print("Logging out...")
            #     break
            # else:
            #     print("Invalid choice")

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
            print("1. View Medicine Prescriptions")
            print("2. Update Medicine Stock")
            print("3. Logout")
            choice = input("Enter choice: ")

            # if choice == "1":
            #     MedicineManagementLib.view_prescriptions()
            # elif choice == "2":
            #     MedicineManagementLib.update_stock()
            # elif choice == "3":
            #     print("Logging out...")
            #     break
            # else:
            #     print("Invalid choice")
