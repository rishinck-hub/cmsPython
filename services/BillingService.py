from models.Billing import Bill
from dao.BillingDaoImpl import BillDAOImpl

class BillMenu:
    @staticmethod
    def show_menu():
        """Bill Management submenu"""
        bill_service = BillService()
        while True:
            print("\n" + "="*50)
            print("             BILL MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Add New Bill")
            print("2. List All Bills")
            print("3. Search Bill by ID")
            print("0. Return to Main Menu")
            print("-"*50)
            
            choice = input("Enter your choice (0-3): ").strip()
            
            if choice == '1':
                bill_service.add_bill()
            elif choice == '2':
                bill_service.list_bills()
            elif choice == '3':
                bill_service.search_bill_by_id()
            elif choice == '0':
                print("Returning to main menu...")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 0 and 3.")

class BillService:
    def __init__(self):
        self.dao = BillDAOImpl()

    def add_bill(self):
        try:
            print("\n--- Add New Bill ---")
            
            # Step 1: Get and validate Patient ID
            while True:
                try:
                    patient_id = int(input("Enter Patient ID: "))
                    if patient_id <= 0:
                        print("❌ Error: Patient ID must be a positive number.")
                        continue
                    if not self.dao.validate_patient_exists(patient_id):
                        print(f"❌ Error: Patient with ID {patient_id} not found or inactive.")
                        continue
                    break
                except ValueError:
                    print("❌ Error: Please enter a valid Patient ID.")
            
            # Step 2: Get and validate Appointment ID
            while True:
                try:
                    appointment_id = int(input("Enter Appointment ID: "))
                    if appointment_id <= 0:
                        print("❌ Error: Appointment ID must be a positive number.")
                        continue
                    # Check if appointment exists
                    if not self.dao.validate_appointment_exists(appointment_id, patient_id):
                        print(f"❌ Error: Appointment {appointment_id} not found for Patient {patient_id}.")
                        continue
                    # Check if appointment already has a bill (one bill per appointment)
                    if not self.dao.validate_appointment_no_existing_bill(appointment_id):
                        print(f"❌ Error: Appointment {appointment_id} already has a bill. One bill per appointment allowed.")
                        continue
                    break
                except ValueError:
                    print("❌ Error: Please enter a valid Appointment ID.")
            
            # Step 3: Get and validate Medicine Prescription ID (strict validation)
            while True:
                medicine_prescription_id = input("Enter Medicine Prescription ID (0 if none): ")
                try:
                    medicine_prescription_id_int = int(medicine_prescription_id) if medicine_prescription_id.strip() else 0
                    if medicine_prescription_id_int < 0:
                        print("❌ Error: Medicine Prescription ID cannot be negative.")
                        continue
                    if not self.dao.validate_medicine_prescription(medicine_prescription_id_int, patient_id):
                        print(f"❌ Error: Medicine Prescription {medicine_prescription_id_int} not found for Patient {patient_id}.")
                        continue
                    break
                except ValueError:
                    print("❌ Error: Please enter a valid Medicine Prescription ID.")
            
            # Step 4: Get and validate Lab Test Prescription ID (strict validation)
            while True:
                labtest_prescription_id = input("Enter Lab Test Prescription ID (0 if none): ")
                try:
                    labtest_prescription_id_int = int(labtest_prescription_id) if labtest_prescription_id.strip() else 0
                    if labtest_prescription_id_int < 0:
                        print("❌ Error: Lab Test Prescription ID cannot be negative.")
                        continue
                    if not self.dao.validate_labtest_prescription(labtest_prescription_id_int, patient_id):
                        print(f"❌ Error: Lab Test Prescription {labtest_prescription_id_int} not found for Patient {patient_id}.")
                        continue
                    break
                except ValueError:
                    print("❌ Error: Please enter a valid Lab Test Prescription ID.")
            
            # Step 5: Get consultation fee automatically from doctors table (NO DEFAULT)
            consultation_fee = self.dao.get_consultation_fee_by_appointment(appointment_id)
            if consultation_fee is None:
                print(f"\n❌ Error: Cannot fetch consultation fee for Appointment {appointment_id}.")
                print("Please ensure the appointment has a valid doctor assigned.")
                return
            
            print(f"\n✅ Consultation Fee (from doctor): ₹{consultation_fee:.2f}")
            
            # Step 6: Get medicine amount automatically from quantity * unitprice
            medicine_cost = self.dao.get_medicine_amount_by_prescription(medicine_prescription_id_int)
            if medicine_prescription_id_int > 0:
                print(f"✅ Medicine Amount (quantity × unit price): ₹{medicine_cost:.2f}")
            
            # Step 7: Get lab test cost (validate numeric input)
            while True:
                try:
                    labtest_input = input("Enter Lab Test Cost (0 if none): ").strip()
                    labtest_cost = float(labtest_input) if labtest_input else 0.0
                    if labtest_cost < 0:
                        print("❌ Error: Lab Test Cost cannot be negative.")
                        continue
                    break
                except ValueError:
                    print("❌ Error: Please enter a valid Lab Test Cost.")
            
            # Create bill with total amount for database compatibility
            total_amount = consultation_fee + medicine_cost + labtest_cost
            bill = Bill(
                0, patient_id, appointment_id,
                medicine_prescription_id_int, labtest_prescription_id_int,
                consultation_fee, medicine_cost, labtest_cost, total_amount
            )
            
            print(f"\n--- Bill Summary ---")
            print(f"Patient ID: {patient_id}")
            print(f"Appointment ID: {appointment_id}")
            print(f"Consultation Fee: ₹{consultation_fee:.2f}")
            print(f"Medicine Cost: ₹{medicine_cost:.2f}")
            print(f"Lab Test Cost: ₹{labtest_cost:.2f}")
            print(f"Total Amount: ₹{total_amount:.2f}")
            
            confirm = input("\nConfirm to save this bill? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Bill creation cancelled.")
                return

            saved_bill = self.dao.add_bill(bill)
            print("\n✅ Bill Added Successfully!")
            print(saved_bill)
        except Exception as e:
            print(f"❌ Error adding bill: {e}")

    def list_bills(self):
        try:
            bills = self.dao.get_all_bills()
            if not bills:
                print("No bills found.")
            else:
                print("\n--- List of Bills ---")
                for bill in bills:
                    print(bill)
        except Exception as e:
            print(f"❌ Error retrieving bills: {e}")

    def search_bill(self):
        try:
            while True:
                try:
                    bill_id = int(input("Enter Bill ID: "))
                    if bill_id <= 0:
                        print("❌ Error: Bill ID must be a positive number.")
                        continue
                    break
                except ValueError:
                    print("❌ Error: Please enter a valid Bill ID.")
            
            bill = self.dao.get_bill_by_id(bill_id)
            if bill:
                print("\n--- Bill Found ---")
                print(bill)
            else:
                print(f"❌ Bill with ID {bill_id} not found.")
        except Exception as e:
            print(f"❌ Error searching for bill: {e}")
