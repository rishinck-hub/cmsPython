from dao.MedicinePrescriptionDao import MedicinePrescriptionDaoService
from db.db_connection import DBConnection
from models.MedicinePrescription import MedicinePrescription
from typing import List

class MedicinePrescriptionDaoImplementation(MedicinePrescriptionDaoService):
    'Implementation for abstract class'

    # SQL Queries
    DISPLAY_ALL = "SELECT * FROM medicineprescriptions"
    INSERT = """INSERT INTO medicineprescriptions
                (medicineid, dosage, frequency, duration, quantity, appointmentid)
                VALUES (%s,%s,%s,%s,%s,%s)"""
    FIND_BY_ID = "SELECT * FROM medicineprescriptions WHERE medicineprescriptionid=%s"
    UPDATE = """UPDATE medicineprescriptions 
                SET medicineid=%s, dosage=%s, frequency=%s, duration=%s, quantity=%s, appointmentid=%s
                WHERE medicineprescriptionid=%s"""
    DELETE = "DELETE FROM medicineprescriptions WHERE medicineprescriptionid=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert_prescription(self, prescription: MedicinePrescription) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.INSERT, (
                prescription.medicine_id,
                prescription.dosage,
                prescription.frequency,
                prescription.duration,
                prescription.quantity,
                prescription.appointment_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting prescription:", e)
            return False
        finally:
            cursor.close()

    def display_all_prescriptions(self) -> List[MedicinePrescription]:
        prescriptions = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                prescriptions.append(MedicinePrescription(
                    medicine_prescription_id=row['medicine_prescription_id'],
                    medicine_id=row['medicine_id'],
                    dosage=row['dosage'],
                    frequency=row['frequency'],
                    duration=row['duration'],
                    quantity=row['quantity'],
                    appointmnent_id=row['appointment_id']
                ))
        except Exception as e:
            print("Error while displaying prescriptions:", e)
        finally:
            cursor.close()
        return prescriptions

    def find_by_id(self, prescription_id: int) -> MedicinePrescription:
        prescription = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.FIND_BY_ID, (prescription_id,))
            row = cursor.fetchone()
            if row:
                prescription = MedicinePrescription(
                    medicine_prescription_id=row['medicine_prescription_id'],
                    medicine_id=row['medicine_id'],
                    dosage=row['dosage'],
                    frequency=row['frequency'],
                    duration=row['duration'],
                    quantity=row['quantity'],
                    appointmnent_id=row['appointment_id']
                )
        except Exception as e:
            print("Error finding prescription:", e)
        finally:
            cursor.close()
        return prescription

    def update_prescription(self, prescription: MedicinePrescription, prescription_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.UPDATE, (
                prescription.medicine_id,
                prescription.dosage,
                prescription.frequency,
                prescription.duration,
                prescription.quantity,
                prescription.appointment_id,
                prescription_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating prescription:", e)
            return False
        finally:
            cursor.close()

    def delete_prescription(self, prescription: MedicinePrescription, prescription_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DELETE, (prescription_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error deleting prescription:", e)
            return False
        finally:
            cursor.close()
