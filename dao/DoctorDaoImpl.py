
from typing import List
from models.Doctor import Doctor
from dao.DoctorDao import DoctorDaoService
from db.db_connection import DBConnection


class DoctorDaoImplementation(DoctorDaoService):
    INSERT_DOCTOR = "INSERT INTO doctors (consultationfee, specializationid, stafffid, isactive) VALUES (%s, %s, %s, %s)"
    DISPLAY_ALL = "SELECT * FROM doctors"
    def __init__(self):
        self.conn = DBConnection().get_connection()
       

    def insert_doctor(self, doctor: Doctor) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.INSERT_DOCTOR, (
                doctor.consultation_fee,
                doctor.specializationid,
                doctor.staffid,
                doctor.isactive
            ))
            self.conn.commit()

            if cursor.rowcount == 1:
                doctor.doctorid = cursor.lastrowid   
                return True
            return False
        except Exception as e:
            print("Error inserting doctor:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def display_all_doctors(self) -> List[Doctor]:
        doctors = []
        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                doctors.append(Doctor(
                    doctorid=row["doctorid"],
                    consultation_fee=row["consultationfee"],
                    specializationid=row["specializationid"],
                    staffid=row["stafffid"],
                    isactive=row["isactive"]
                ))
        except Exception as e:
            print("Error fetching doctors:", e)
        finally:
            if cursor:
                cursor.close()
        return doctors
    
    
    def find_by_id(self, doctorid: int) -> Doctor:
        cursor = None
        try:
          cursor = self.conn.cursor(dictionary=True)
          query = "SELECT * FROM doctors WHERE doctorid = %s"
          cursor.execute(query, (doctorid,))
          row = cursor.fetchone()

          if row:
            return Doctor(
                doctorid=row["doctorid"],
                consultation_fee=row["consultationfee"],  
                specializationid=row["specializationid"],
                staffid=row["stafffid"],                    
                isactive=row["isactive"]
            )
          return None

        except Exception as e:
          print("Error searching doctor by ID:", e)
          return None

        finally:
         if cursor:
            cursor.close()

    def disable_doctor(self, doctorid: int) -> bool:
       cursor = None
       try:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE doctors SET isactive = %s WHERE doctorid = %s", ("N", doctorid))
        self.conn.commit()
        return cursor.rowcount > 0
       except Exception as e:
        print("Error disabling doctor:", e)
        return False
       finally:
        if cursor:
            cursor.close()



    
