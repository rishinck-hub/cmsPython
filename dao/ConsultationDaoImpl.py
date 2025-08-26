from dao.ConsultationDao import ConsultationDaoService
from db.db_connection import DBConnection
from models.Consultation import Consultation
from typing import List

class ConsultationDaoImplementation(ConsultationDaoService):
    DISPLAY_ALL = "SELECT * FROM consultations"
    INSERT_CONSULTATION = """INSERT INTO consultations
        (symptoms, diagnosis, createddate, appointmentid)
        VALUES (%s, %s, %s, %s)"""
    FIND_BY_ID = "SELECT * FROM consultations WHERE consultationid=%s"
    UPDATE_CONSULTATION = """UPDATE consultations 
        SET symptoms=%s, diagnosis=%s, createddate=%s, appointmentid=%s
        WHERE consultationid=%s"""
    DELETE_CONSULTATION = "DELETE FROM consultations WHERE consultationid=%s"
    DISPLAY_CONSULTATION = "SELECT * FROM consultations WHERE consultationid=%s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def insert_consultation(self, consultation: Consultation) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.INSERT_CONSULTATION, (
                consultation.symptoms,
                consultation.diagnosis,
                consultation.created_date,
                consultation.appointment_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting consultation:", e)
            return False
        finally:
            cursor.close()

    def display_all_consultations(self) -> List[Consultation]:
        consultations = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                consultations.append(Consultation(
                    consultationid=row['consultation_id'],
                    symptoms=row['symptoms'],
                    diagnosis=row['diagnosis'],
                    createddate=row['created_date'],
                    appointmentid=row['appointment_id']
                ))
        except Exception as e:
            print("Error displaying consultations:", e)
        finally:
            cursor.close()
        return consultations

    def find_by_consultation_id(self, consultation_id: int):
        consultation = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.FIND_BY_ID, (consultation_id,))
            row = cursor.fetchone()
            if row:
                consultation = Consultation(
                    consultationid=row['consultation_id'],
                    symptoms=row['symptoms'],
                    diagnosis=row['diagnosis'],
                    createddate=row['created_date'],
                    appointmentid=row['appointment_id']
                )
        except Exception as e:
            print("Error finding consultation:", e)
        finally:
            cursor.close()
        return consultation

    def update_consultation(self, consultation: Consultation, consultation_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.UPDATE_CONSULTATION, (
                consultation.symptoms,
                consultation.diagnosis,
                consultation.created_date,
                consultation.appointment_id,
                consultation_id
            ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating consultation:", e)
            return False
        finally:
            cursor.close()

    def delete_consultation(self, consultation: Consultation, consultation_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.DELETE_CONSULTATION, (consultation_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error deleting consultation:", e)
            return False
        finally:
            cursor.close()

    def display_consultation(self, consultation, consultation_id):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.DISPLAY_CONSULTATION, (consultation_id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            print("Error displaying consultation:", e)
            return None
        finally:
            cursor.close()
