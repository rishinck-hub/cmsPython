from dao.StaffDaoImpl import StaffDaoImplementation
from dao.StaffDao import StaffDaoService
from datetime import datetime
from models.Staff import Staff

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
        roleid = input("Enter Role ID (1.Admin 2.Doctor, 3.Receptionalist, 4.Pharmacist): ")
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
    
    staticmethod
    def edit_staff_name(staff, new_name):
        if len(new_name) < 3:
            print(" Name must have at least 3 characters")
            return False

        staff.set_fullname(new_name)
        StaffManagementLib.dao_service.update_staff_name(staff)
        print(" Name updated successfully!")
        return True
    
    