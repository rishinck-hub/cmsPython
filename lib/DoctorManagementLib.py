
from models.Doctor import Doctor
from dao.DoctorDao import DoctorDaoService
from dao.DoctorDaoImpl import DoctorDaoImplementation

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


    