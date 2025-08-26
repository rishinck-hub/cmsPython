from dao.MedicinePrescriptionDao import MedicinePrescriptionDaoService
from dao.MedicinePrescriptionDaoImpl import MedicinePrescriptionDaoImplementation
from models.MedicinePrescription import MedicinePrescription
from dao.ConsultationDaoImpl import ConsultationDaoImplementation
from dao.ConsultationDao import ConsultationDaoService
from models.Consultation import Consultation
from dao.LabTestPrescriptionDao import LabTestPrescriptionDaoService
from dao.LabTestPrescriptionDaoImpl import LabTestPrescriptionDaoImplementation
from models.LabTestPrescription import LabTestPrescription
from services.ConsultationService import LabTestPrescriptionValidation
from services.ConsultationService import ConsultationValidation
from datetime import datetime

'''Consulatation operations'''
class ConsultationManagementLib:
    'Handles CRUD logic for Consultation'
    dao_service: ConsultationDaoService = ConsultationDaoImplementation()

    @staticmethod
    def display_all():
        consultations = ConsultationManagementLib.dao_service.display_all_consultations()
        for c in consultations:
            print(c)

    @staticmethod
    def add_consultation():
        try:
            while True:
                symptoms = input("Enter Symptoms: ")
                if ConsultationValidation.validate_symptoms(symptoms):
                    break
                else:
                    print("Invalid Symptoms! Cannot be empty.")

            while True:
                diagnosis = input("Enter Diagnosis: ")
                if ConsultationValidation.validate_diagnosis(diagnosis):
                    break
                else:
                    print("Invalid Diagnosis! Cannot be empty.")

            while True:
                date_str = input("Enter Created Date (dd/mm/yyyy): ")
                if ConsultationValidation.validate_date_string(date_str):
                    created_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                    break
                else:
                    print("Invalid Date! Must be in format dd/mm/yyyy and not in the future.")

            while True:
                try:
                    appointment_id = int(input("Enter Appointment ID: "))
                    if ConsultationValidation.validate_appointment_id(appointment_id):
                        break
                    else:
                        print("Invalid Appointment ID! Must be a positive integer.")
                except Exception:
                    print("Appointment ID must be an integer.")

            consultation = Consultation(
                symptoms=symptoms,
                diagnosis=diagnosis,
                createddate=created_date,
                appointmentid=appointment_id
            )

            if ConsultationManagementLib.dao_service.insert_consultation(consultation):
                print("Consultation inserted successfully!")
            else:
                print("Something went wrong while inserting consultation.")

        except Exception as e:
            print("Error:", e)

    @staticmethod
    def update_consultation():
        try:
            searchid = int(input("Enter Consultation ID to update: "))
            consultation = ConsultationManagementLib.dao_service.find_by_consultation_id(searchid)
            if not consultation:
                print("Consultation not found!")
                return
            print(consultation)

            confirm = input("Do you want to edit this data? (y/n): ")
            if confirm.lower() == "y":
                while True:
                    symptoms = input("Enter Symptoms: ")
                    if ConsultationValidation.validate_symptoms(symptoms):
                        consultation.symptoms = symptoms
                        break
                    else:
                        print("Invalid Symptoms!")

                while True:
                    diagnosis = input("Enter Diagnosis: ")
                    if ConsultationValidation.validate_diagnosis(diagnosis):
                        consultation.diagnosis = diagnosis
                        break
                    else:
                        print("Invalid Diagnosis!")

                while True:
                    date_str = input("Enter Created Date (dd/mm/yyyy): ")
                    if ConsultationValidation.validate_date_string(date_str):
                        consultation.created_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                        break
                    else:
                        print("Invalid Date!")

                while True:
                    try:
                        appointment_id = int(input("Enter Appointment ID: "))
                        if ConsultationValidation.validate_appointment_id(appointment_id):
                            consultation.appointment_id = appointment_id
                            break
                        else:
                            print("Invalid Appointment ID!")
                    except Exception:
                        print("Appointment ID must be an integer.")

                if ConsultationManagementLib.dao_service.update_consultation(consultation, searchid):
                    print("Consultation updated successfully!")
                else:
                    print("Error updating consultation.")

        except Exception as e:
            print("Error:", e)

    @staticmethod
    def delete_consultation():
        try:
            searchid = int(input("Enter Consultation ID to delete: "))
            consultation = ConsultationManagementLib.dao_service.find_by_consultation_id(searchid)
            if not consultation:
                print("Consultation not found!")
                return
            print(consultation)
            confirm = input("Do you want to delete this Consultation? (y/n): ")
            if confirm.lower() == "y":
                if ConsultationManagementLib.dao_service.delete_consultation(consultation, searchid):
                    print("Consultation deleted successfully!")
                else:
                    print("Error deleting consultation.")
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def display_one():
        try:
            searchid = int(input("Enter Consultation ID to display: "))
            consultation = ConsultationManagementLib.dao_service.find_by_consultation_id(searchid)
            if not consultation:
                print("Consultation not found!")
                return
            print(consultation)
        except Exception as e:
            print("Error:", e)


'''Medicine Prescription operations'''
class MedicinePrescriptionManagementLib:
    'Handles CRUD logic for Medicine Prescription'
    dao_service: MedicinePrescriptionDaoService = MedicinePrescriptionDaoImplementation()

    @staticmethod
    def display_all():
        prescriptions = MedicinePrescriptionManagementLib.dao_service.display_all_prescriptions()
        for p in prescriptions:
            print(p)

    @staticmethod
    def add_prescription():
        try:
            while True:
                try:
                    medicine_id = int(input("Enter Medicine ID: "))
                    if ConsultationValidation.validate_medicine_id(medicine_id):
                        break
                    else:
                        print("Invalid Medicine ID! Must be a positive integer.")
                except Exception:
                    print("Medicine ID must be an integer.")

            while True:
                dosage = input("Enter Dosage (e.g. 500mg, 2 tablets): ")
                if ConsultationValidation.validate_dosage(dosage):
                    break
                else:
                    print("Invalid Dosage! Cannot be empty.")

            while True:
                frequency = input("Enter Frequency (e.g. 2 times a day): ")
                if ConsultationValidation.validate_frequency(frequency):
                    break
                else:
                    print("Invalid Frequency! Cannot be empty.")

            while True:
                duration = input("Enter Duration (e.g. 5 days): ")
                if ConsultationValidation.validate_duration(duration):
                    break
                else:
                    print("Invalid Duration! Cannot be empty.")

            while True:
                try:
                    quantity = int(input("Enter Quantity: "))
                    if ConsultationValidation.validate_quantity(quantity):
                        break
                    else:
                        print("Invalid Quantity! Must be positive.")
                except Exception:
                    print("Quantity must be an integer.")

            while True:
                try:
                    appointment_id = int(input("Enter Appointment ID: "))
                    if ConsultationValidation.validate_appointment_id(appointment_id):
                        break
                    else:
                        print("Invalid Appointment ID! Must be a positive integer.")
                except Exception:
                    print("Appointment ID must be an integer.")

            prescription = MedicinePrescription(
                medicine_id=medicine_id,
                dosage=dosage,
                frequency=frequency,
                duration=duration,
                quantity=quantity,
                appointmnent_id=appointment_id
            )

            if MedicinePrescriptionManagementLib.dao_service.insert_prescription(prescription):
                print("Prescription inserted successfully!")
            else:
                print("Something went wrong while inserting prescription.")

        except Exception as e:
            print("Error:", e)

    @staticmethod
    def update_prescription():
        try:
            searchid = int(input("Enter Prescription ID to update: "))
            prescription = MedicinePrescriptionManagementLib.dao_service.find_by_id(searchid)
            if not prescription:
                print("Prescription not found!")
                return
            print(prescription)
            confirm = input("Do you want to edit this data? (y/n): ")
            if confirm.lower() == "y":
                while True:
                    try:
                        medicine_id = int(input("Enter Medicine ID: "))
                        if ConsultationValidation.validate_medicine_id(medicine_id):
                            prescription.medicine_id = medicine_id
                            break
                        else:
                            print("Invalid Medicine ID!")
                    except Exception:
                        print("Medicine ID must be an integer.")

                while True:
                    dosage = input("Enter Dosage: ")
                    if ConsultationValidation.validate_dosage(dosage):
                        prescription.dosage = dosage
                        break
                    else:
                        print("Invalid Dosage!")

                while True:
                    frequency = input("Enter Frequency: ")
                    if ConsultationValidation.validate_frequency(frequency):
                        prescription.frequency = frequency
                        break
                    else:
                        print("Invalid Frequency!")

                while True:
                    duration = input("Enter Duration: ")
                    if ConsultationValidation.validate_duration(duration):
                        prescription.duration = duration
                        break
                    else:
                        print("Invalid Duration!")

                while True:
                    try:
                        quantity = int(input("Enter Quantity: "))
                        if ConsultationValidation.validate_quantity(quantity):
                            prescription.quantity = quantity
                            break
                        else:
                            print("Invalid Quantity!")
                    except Exception:
                        print("Quantity must be an integer.")

                while True:
                    try:
                        appointment_id = int(input("Enter Appointment ID: "))
                        if ConsultationValidation.validate_appointment_id(appointment_id):
                            prescription.appointment_id = appointment_id
                            break
                        else:
                            print("Invalid Appointment ID!")
                    except Exception:
                        print("Appointment ID must be an integer.")

                if MedicinePrescriptionManagementLib.dao_service.update_prescription(prescription, searchid):
                    print("Prescription updated successfully!")
                else:
                    print("Error updating prescription.")
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def delete_prescription():
        try:
            searchid = int(input("Enter Prescription ID to delete: "))
            prescription = MedicinePrescriptionManagementLib.dao_service.find_by_id(searchid)
            if not prescription:
                print("Prescription not found!")
                return
            print(prescription)
            confirm = input("Do you want to delete this Prescription? (y/n): ")
            if confirm.lower() == "y":
                if MedicinePrescriptionManagementLib.dao_service.delete_prescription(prescription, searchid):
                    print("Prescription deleted successfully!")
                else:
                    print("Error deleting prescription.")
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def display_one():
        try:
            searchid = int(input("Enter Prescription ID to display: "))
            prescription = MedicinePrescriptionManagementLib.dao_service.find_by_id(searchid)
            if not prescription:
                print("Prescription not found!")
                return
            print(prescription)
        except Exception as e:
            print("Error:", e)

'''labtest Prescription Management library'''
class LabTestPrescriptionManagementLib:
    'Handles CRUD logic for LabTestPrescription'
    dao_service: LabTestPrescriptionDaoService = LabTestPrescriptionDaoImplementation()

    @staticmethod
    def display_all():
        prescriptions = LabTestPrescriptionManagementLib.dao_service.display_all_prescriptions()
        for prescription in prescriptions:
            print(prescription)

    @staticmethod
    def add_prescription():
        prescription_id = None
        while True:
            try:
                labtest_id = int(input("Enter LabTest ID: "))
                break
            except Exception as e:
                print("Invalid input for LabTest ID:", e)

        while True:
            created = input("Enter Created Date (dd/mm/yyyy): ")
            util_date = datetime.strptime(created, "%d/%m/%Y")
            convdate = util_date.date()
            if LabTestPrescriptionValidation.validate_created_date(convdate):
                created_date = convdate
                break
            else:
                print("Invalid date! Must not be in future.")

        remarks = input("Enter remarks: ")
        while not LabTestPrescriptionValidation.validate_remarks(remarks):
            print("Invalid remarks! Must be at least 3 characters.")
            remarks = input("Enter remarks again: ")

        while True:
            try:
                appointment_id = int(input("Enter Appointment ID: "))
                break
            except Exception as e:
                print("Invalid Appointment ID:", e)

        prescription = LabTestPrescription(prescription_id, labtest_id, created_date, remarks, appointment_id)
        if LabTestPrescriptionManagementLib.dao_service.insert_prescription(prescription):
            print("Prescription inserted successfully!")
        else:
            print("Something went wrong!")

    @staticmethod
    def update_prescription():
        searchid = int(input("Enter prescription ID to update: "))
        prescription = LabTestPrescriptionManagementLib.dao_service.find_by_id(searchid)
        if not prescription:
            print("Prescription not found!")
            return
        print(prescription)

        confirm = input("Do you want to edit this data? (y/n): ")
        if confirm.lower() == "y":
            try:
                labtest_id = int(input("Enter LabTest ID: "))
                created = input("Enter Created Date (dd/mm/yyyy): ")
                created_date = datetime.strptime(created, "%d/%m/%Y").date()
                remarks = input("Enter remarks: ")
                appointment_id = int(input("Enter Appointment ID: "))

                prescription.labtest_id = labtest_id
                prescription.created_date = created_date
                prescription.remarks = remarks
                prescription.appointment_id = appointment_id

                if LabTestPrescriptionManagementLib.dao_service.update_labtest_prescription(prescription, searchid):
                    print("Updated successfully!")
                else:
                    print("Update failed!")
            except Exception as e:
                print("Error updating prescription:", e)

    @staticmethod
    def delete_prescription():
        searchid = int(input("Enter prescription ID to delete: "))
        prescription = LabTestPrescriptionManagementLib.dao_service.find_by_id(searchid)
        if not prescription:
            print("Prescription not found!")
            return
        print(prescription)

        confirm = input("Do you want to delete this prescription? (y/n): ")
        if confirm.lower() == "y":
            if LabTestPrescriptionManagementLib.dao_service.delete_prescription(prescription, searchid):
                print("Prescription deleted successfully!")
            else:
                print("Delete failed!")

    @staticmethod
    def display_one():
        searchid = int(input("Enter prescription ID to display: "))
        prescription = LabTestPrescriptionManagementLib.dao_service.find_by_id(searchid)
        if not prescription:
            print("Prescription not found!")
            return
        print(prescription)
