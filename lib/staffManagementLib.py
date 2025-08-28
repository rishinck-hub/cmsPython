from dao.StaffDaoImpl import StaffDaoImplementation
from dao.StaffDao import StaffDaoService
from datetime import datetime
from models.Staff import Staff
from models.Doctor import Doctor
from dao.DoctorDao import DoctorDaoService
from dao.DoctorDaoImpl import DoctorDaoImplementation


class StaffManagementLib:

    dao_service:StaffDaoService = StaffDaoImplementation()
    
    @staticmethod
    def add_staff():
        staff = Staff()
        fullname = input("Enter Full Name: ")
        staff.set_fullname(fullname)
        gender = input("Enter Gender (male/female): ")
        staff.set_gender(gender)
        bloodgroup = input("Enter Blood Group: ")
        staff.set_bloodgroup(bloodgroup)
        mobileno = input("Enter Mobile No (10 digits): ")
        staff.set_mobileno(mobileno)
        dob = input("Enter Date of Birth (dd/mm/yyyy): ")
        staff.set_dob(dob)
        username = input("Enter Username (min 6 chars): ")
        staff.set_username(username)
        password = input("Enter Password (min 6 chars): ")
        staff.set_password(password)
        roleid = input("Enter Role ID (1.Admin, 2.Doctor, 3.Receptionalist, 4.Pharmacist): ")
        staff.set_roleid(roleid)
        staff.set_isactive(isactive="Y")

        if StaffManagementLib.dao_service.insert_staff(staff):
           print(f"Successfully Added Staff: SATFF ID:{staff.get_staffid()}....")       
        else:
            print("Something went wrong.......")  

    @staticmethod
    def display_all():
        staffs = StaffManagementLib.dao_service.display_all_staffs()
        for staff in staffs:
            print(staff)

    @staticmethod
    def search_by_staffid():
        staffid = input("Enter Staff Number: ")
        staff = StaffManagementLib.dao_service.find_by_staffid(staffid)
        if staff:
            return staff
        else:
            print(" Sorry, there is no such staff.")
            return None

    @staticmethod
    def search_by_mobileno():
        mobileno = input("Enter Phone Number: ")
        staff = StaffManagementLib.dao_service.find_by_mobileno(mobileno)
        if staff:
            return staff
        else:
            print(" Sorry, there is no such staff.")
            return None
            
    @staticmethod
    def disable_staff(staff: Staff):
        staff.set_isactive("N")
        if StaffManagementLib.dao_service.disable_staff(staff.get_staffid()):
            print(" Staff disabled successfully!")
        else:
            print(" Failed to disable staff.")

    @staticmethod
    def update_staff_name(staff, new_name):
        if len(new_name) < 3:
            print(" Name must have at least 3 characters")
            return False
        staff.set_fullname(new_name)
        StaffManagementLib.dao_service.update_staff_name(staff)
        print(" Updated successfully!")
        return True
    
    @staticmethod
    def update_staff_mobileno(staff, new_mobile):
     if not (new_mobile.isdigit() and len(new_mobile) == 10):
        print(" Mobile number must be exactly 10 digits")
        return False

     staff.set_mobileno(new_mobile)

     if StaffManagementLib.dao_service.update_staff_mobileno(staff):
        print(" Mobile number updated successfully!")
        return True
     else:
        print(" Failed to update mobile number in DB")
        return False

class DoctorManagementLib:
    dao_service: DoctorDaoService = DoctorDaoImplementation()


    @staticmethod
    def add_doctor():
        doctor = Doctor()

        stafffid = input("Enter Staff ID (must be an existing staff): ")
        doctor.staffid = stafffid   # using property

        specializationid = input("Enter Specialization ID: ")
        doctor.specializationid = specializationid

        try:
            consultationfee = float(input("Enter Consultation Fee: "))
            doctor.consultation_fee = consultationfee
        except ValueError:
            print(" Invalid input. Fee must be a number.")
            return

        doctor.isactive = "Y"

        if DoctorManagementLib.dao_service.insert_doctor(doctor):
            print(f" Successfully Added Doctor: DOCTOR ID: {doctor.doctorid}")
        else:
            print(" Something went wrong while adding doctor...")

    @staticmethod
    def list_doctors():
        """List all doctors"""
        doctors = DoctorManagementLib.dao_service.display_all_doctors()
        if not doctors:
            print(" No doctors found")
            return []
        print("\n ========= Doctor List =========")
        for d in doctors:
            print(d)
        return doctors
    
    @staticmethod
    def search_doctor():
        try:
          doctor_id = input("Enter Doctor ID to search: ")

          if not doctor_id.isdigit():
            print(" Invalid Doctor ID! Must be a number.")
            return None

          doctor = DoctorManagementLib.dao_service.find_by_id(int(doctor_id))
          if doctor:
            print("\n ========= Doctor Found =========")
            print(doctor)   
            return doctor
          else:
            print(" Doctor not found")
            return None

        except Exception as e:
          print(" Error while searching doctor:", e)
        return None


    @staticmethod
    def disable_doctor():
        try:
           doctor_id = input("Enter Doctor ID to disable: ")

           if not doctor_id.isdigit():
            print(" Invalid Doctor ID! Must be a number.")
            return False

           doctor_id = int(doctor_id)
           doctor = DoctorManagementLib.dao_service.find_by_id(doctor_id)
           if not doctor:
            print(" Doctor not found!")
            return False

           doctor.isactive = "N"

           if DoctorManagementLib.dao_service.disable_doctor(doctor.doctorid):
            print(" Doctor disabled successfully!")
            return True
           else:
            print(" Failed to disable doctor.")
            return False

        except Exception as e:
           print(" Error while disabling doctor:", e)
        return False


    
    