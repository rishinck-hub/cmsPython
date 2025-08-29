from dao.BillingDao import BillDAO
from db.db_connection import DBConnection
from models.Billing import Bill
from datetime import datetime, date

class BillDAOImpl:
    def __init__(self):
        db_connection = DBConnection()
        self.conn = db_connection.connection
        self.cursor = self.conn.cursor(dictionary=True)



    # Add Bill
    def add_bill(self, bill: Bill):
        # Check if the billing table is empty
        self.cursor.execute("SELECT COUNT(*) as count FROM billing")
        count = self.cursor.fetchone()['count']
        
        # If table is empty, reset auto-increment counter
        if count == 0:
            self.cursor.execute("ALTER TABLE billing AUTO_INCREMENT = 1")
        
        # Include all the cost components that user entered
        query = """
        INSERT INTO billing (patientid, appointmentid, medicineprescriptionid, labtestprescriptionid, 
                           consultationfee, medicineamount, labtestamount)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # Handle prescription IDs - use NULL if 0 or None
        medicine_id = bill.get_medicine_prescription_id() if bill.get_medicine_prescription_id() != 0 else None
        labtest_id = bill.get_labtest_prescription_id() if bill.get_labtest_prescription_id() != 0 else None
        
        values = (bill.get_patient_id(), bill.get_appointment_id(), medicine_id, labtest_id,
                 bill.get_consultation_fee(), bill.get_medicine_cost(), bill.get_labtest_cost())
        
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            bill.bill_id = self.cursor.lastrowid
            
            # Fetch the complete bill with generated totalamount
            return self.get_bill_by_id(bill.bill_id)
        except Exception as e:
            self.conn.rollback()
            raise e

    # Get all bills
    def get_all_bills(self):
        query = "SELECT * FROM billing"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        bills = []
        for row in rows:
            # Use correct column names from database and handle NULL values
            consultation_fee = row.get("consultationfee") or 0.00
            medicine_cost = row.get("medicineamount") or 0.00
            labtest_cost = row.get("labtestamount") or 0.00
            total_amount = row.get("totalamount") or (consultation_fee + medicine_cost + labtest_cost)
            
            bills.append(
                Bill(row["billingid"], row["patientid"], row["appointmentid"],
                     row["medicineprescriptionid"], row["labtestprescriptionid"],
                     consultation_fee, medicine_cost, labtest_cost, total_amount)
            )
        return bills

    # Get bill by ID
    def get_bill_by_id(self, bill_id: int):
        query = "SELECT * FROM billing WHERE billingid = %s"
        self.cursor.execute(query, (bill_id,))
        row = self.cursor.fetchone()
        if row:
            # Use correct column names from database and handle NULL values
            consultation_fee = row.get("consultationfee") or 0.00
            medicine_cost = row.get("medicineamount") or 0.00
            labtest_cost = row.get("labtestamount") or 0.00
            total_amount = row.get("totalamount") or (consultation_fee + medicine_cost + labtest_cost)
            
            return Bill(row["billingid"], row["patientid"], row["appointmentid"],
                        row["medicineprescriptionid"], row["labtestprescriptionid"],
                        consultation_fee, medicine_cost, labtest_cost, total_amount)
        return None

    # Update Bill Amount
    def update_bill_amount(self, bill_id: int, new_amount: float):
        query = "UPDATE billing SET totalamount = %s WHERE billingid = %s"
        self.cursor.execute(query, (new_amount, bill_id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # Get consultation fee from doctors table based on appointment (NO DEFAULTS)
    def get_consultation_fee_by_appointment(self, appointment_id: int):
        try:
            # Join appointments and doctors table to get consultation fee
            query = """
            SELECT d.consultationfee 
            FROM appointments a 
            JOIN doctors d ON a.doctorid = d.doctorid 
            WHERE a.appointmentid = %s
            """
            self.cursor.execute(query, (appointment_id,))
            result = self.cursor.fetchone()
            if result:
                return float(result['consultationfee'])
            
            # If join fails, try alternative approach by doctor name
            query_alt = """
            SELECT d.consultationfee 
            FROM appointments a, doctors d 
            WHERE a.appointmentid = %s AND a.doctor_name = d.name
            """
            self.cursor.execute(query_alt, (appointment_id,))
            result = self.cursor.fetchone()
            if result:
                return float(result['consultationfee'])
            
            # Return None if no consultation fee found (no defaults)
            return None
        except Exception:
            return None

    # Get medicine amount by calculating quantity * unitprice
    def get_medicine_amount_by_prescription(self, medicine_prescription_id: int):
        try:
            if medicine_prescription_id == 0 or medicine_prescription_id is None:
                return 0.00
            
            # Join medicineprescriptions and medicines tables to calculate amount
            query = """
            SELECT mp.quantity, m.unitprice 
            FROM medicineprescriptions mp 
            JOIN medicines m ON mp.medicineid = m.medicineid 
            WHERE mp.medicineprescriptionid = %s
            """
            self.cursor.execute(query, (medicine_prescription_id,))
            result = self.cursor.fetchone()
            if result:
                quantity = float(result['quantity'])
                unit_price = float(result['unitprice'])
                return quantity * unit_price
            return 0.00
        except Exception as e:
            print(f"Error calculating medicine amount: {e}")
            return 0.00
    
    # Validation: Check if patient exists and is active
    def validate_patient_exists(self, patient_id: int):
        try:
            query = "SELECT patientid FROM patients WHERE patientid = %s AND isactive = TRUE"
            self.cursor.execute(query, (patient_id,))
            return self.cursor.fetchone() is not None
        except Exception:
            return False
    
    # Validation: Check if appointment exists and belongs to the patient
    def validate_appointment_exists(self, appointment_id: int, patient_id: int):
        try:
            query = "SELECT appointmentid FROM appointments WHERE appointmentid = %s AND patientid = %s"
            self.cursor.execute(query, (appointment_id, patient_id))
            return self.cursor.fetchone() is not None
        except Exception:
            return False
    
    # Validation: Check if appointment already has a bill (one bill per appointment)
    def validate_appointment_no_existing_bill(self, appointment_id: int):
        try:
            query = "SELECT billingid FROM billing WHERE appointmentid = %s"
            self.cursor.execute(query, (appointment_id,))
            return self.cursor.fetchone() is None  # Return True if no existing bill
        except Exception:
            return False
    
    # Validation: Check if medicine prescription exists (simplified - just check if ID exists)
    def validate_medicine_prescription(self, medicine_prescription_id: int, patient_id: int):
        try:
            if medicine_prescription_id == 0 or medicine_prescription_id is None:
                return True  # No prescription is valid
            # Just check if prescription exists (don't enforce patient relationship for now)
            query = "SELECT medicineprescriptionid FROM medicineprescriptions WHERE medicineprescriptionid = %s"
            self.cursor.execute(query, (medicine_prescription_id,))
            return self.cursor.fetchone() is not None
        except Exception:
            return False
    
    # Validation: Check if lab test prescription exists (simplified - just check if ID exists)
    def validate_labtest_prescription(self, labtest_prescription_id: int, patient_id: int):
        try:
            if labtest_prescription_id == 0 or labtest_prescription_id is None:
                return True  # No prescription is valid
            # Just check if prescription exists (don't enforce patient relationship for now)
            query = "SELECT labtestprescriptionid FROM labtestprescriptions WHERE labtestprescriptionid = %s"
            self.cursor.execute(query, (labtest_prescription_id,))
            return self.cursor.fetchone() is not None
        except Exception:
            return False

    # Delete Bill
    def delete_bill(self, bill_id: int):
        query = "DELETE FROM billing WHERE billingid = %s"
        self.cursor.execute(query, (bill_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
