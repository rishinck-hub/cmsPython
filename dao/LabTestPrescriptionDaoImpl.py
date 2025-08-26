from dao.LabTestPrescriptionDao import LabTestPrescriptionDaoService

from db.db_connection import DBConnection
from models.LabTestPrescription import LabTestPrescription
from typing import List

class LabTestPrescriptionDaoImplementation(LabTestPrescriptionDaoService):
    'Implementation for abstract LabTestPrescriptionDao'

    # SQL Queries
    DISPLAY_ALL = "SELECT * FROM labtestprescriptions"
    INSERT_PRESCRIPTION = "INSERT INTO labtestprescriptions(labtestid, createddate, remarks, appointmentid) VALUES(%s, %s, %s, %s)"
    FIND_BY_ID = "SELECT * FROM labtestprescriptions WHERE labtestprescriptionid=%s"
    UPDATE_PRESCRIPTION = "UPDATE labtestprescriptions SET labtestid=%s, createddate=%s, remarks=%s, appointmentid=%s WHERE labtestprescriptionid=%s"
    DELETE_PRESCRIPTION = "DELETE FROM labtestprescriptions WHERE labtestprescriptionid=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert_prescription(self, prescription: LabTestPrescription) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.INSERT_PRESCRIPTION, (
                prescription.labtest_id,
                prescription.created_date,
                prescription.remarks,
                prescription.appointment_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting LabTestPrescription:", e)
            return False
        finally:
            cursor.close()

    def display_all_prescriptions(self) -> List[LabTestPrescription]:
        prescriptions = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                prescriptions.append(LabTestPrescription(
                    labtest_prescription_id=row['labtest_prescription_id'],
                    labtest_id=row['labtest_id'],
                    created_date=row['created_date'],
                    remarks=row['remarks'],
                    appointment_id=row['appointment_id']
                ))
        except Exception as e:
            print("Error displaying LabTestPrescriptions:", e)
        finally:
            cursor.close()
        return prescriptions

    def find_by_id(self, labtest_prescription_id: int) -> LabTestPrescription:
        prescription = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.FIND_BY_ID, (labtest_prescription_id,))
            row = cursor.fetchone()
            if row:
                prescription = LabTestPrescription(
                    labtest_prescription_id=row['labtest_prescription_id'],
                    labtest_id=row['labtest_id'],
                    created_date=row['created_date'],
                    remarks=row['remarks'],
                    appointment_id=row['appointment_id']
                )
        except Exception as e:
            print("Error finding LabTestPrescription:", e)
        finally:
            cursor.close()
        return prescription

    def update_prescription(self, prescription: LabTestPrescription, labtest_prescription_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.UPDATE_PRESCRIPTION, (
                prescription.labtest_id,
                prescription.created_date,
                prescription.remarks,
                prescription.appointment_id,
                labtest_prescription_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating LabTestPrescription:", e)
            return False
        finally:
            cursor.close()

    def delete_prescription(self, prescription: LabTestPrescription, labtest_prescription_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DELETE_PRESCRIPTION, (labtest_prescription_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error deleting LabTestPrescription:", e)
            return False
        finally:
            cursor.close()
