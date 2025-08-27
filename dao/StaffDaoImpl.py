from dao.StaffDao import StaffDaoService
from db.db_connection import DBConnection
from typing import List
from models.Staff import Staff
from datetime import date,datetime


class StaffDaoImplementation(StaffDaoService):
    DISPLAY_ALL = "SELECT * from staffs"
    INSERT_STAFF = "INSERT INTO staffs(fullname,gender,bloodgroup,mobileno,dob,username,password,roleid,isactive) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)"
    FIND_BY_ID = "SELECT * FROM staffs WHERE staffid = %s"
    FIND_BY_MOBILE = "SELECT * FROM staffs WHERE mobileno = %s"

    def __init__(self):
        self.conn = DBConnection().get_connection()



    def insert_staff(self,staff:Staff)->bool:
        try:
            cursor = self.conn.cursor()

            dob = staff.get_dob()
            if isinstance(dob, (datetime, date)):
                dob = dob.strftime("%Y-%m-%d")

            cursor.execute(self.INSERT_STAFF,(
                staff.get_fullname(),
                staff.get_gender(),
                staff.get_bloodgroup(),
                staff.get_mobileno(),
                dob,  # convert date to str
                staff.get_username(),
                staff.get_password(),
                staff.get_roleid(),
                staff.get_isactive()
            ))
            self.conn.commit()
            if cursor.rowcount == 1:
              staff_id = cursor.lastrowid   
              staff.set_staffid(staff_id)   
              return True
            return False
        except Exception as e:
           print("Error inserting staff:", e)
           return False
        finally:
          cursor.close()

    def display_all_staffs(self)-> List[Staff]:
        staffs = []
        cursor = None
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                staffs.append(Staff(staffid=row["staffid"],fullname=row["fullname"],
                                    gender=row["gender"],bloodgroup=row["bloodgroup"],
                                    mobileno=row["mobileno"],dob=row["dob"],username=row["username"],
                                    password=row["password"],roleid=row["roleid"],isactive=row["isactive"]))
        except Exception as e:
            print("Error fetching staffs:",e)
        finally:
           if cursor:
            cursor.close()
        return staffs
                       
    def find_by_staffid(self, staffid: int) -> Staff:
        try:
           cursor = self.conn.cursor(dictionary=True)
           cursor.execute(self.FIND_BY_ID, (staffid,))
           row = cursor.fetchone()
           if row:
              return Staff(
                staffid=row["staffid"], fullname=row["fullname"], gender=row["gender"],
                bloodgroup=row["bloodgroup"], mobileno=row["mobileno"], dob=row["dob"],
                username=row["username"], password=row["password"],
                roleid=row["roleid"], isactive=row["isactive"]
               )
           return None
        except Exception as e:
            print("Error searching staff by ID:", e)
            return None
        finally:
             cursor.close()

    def find_by_mobileno(self, mobileno: str) -> Staff:
        try:
           cursor = self.conn.cursor(dictionary=True)
           cursor.execute(self.FIND_BY_MOBILE, (mobileno,))
           row = cursor.fetchone()
           if row:
              return Staff(
                staffid=row["staffid"], fullname=row["fullname"], gender=row["gender"],
                bloodgroup=row["bloodgroup"], mobileno=row["mobileno"], dob=row["dob"],
                username=row["username"], password=row["password"],
                roleid=row["roleid"], isactive=row["isactive"]
            )
           return None
        except Exception as e:
          print("Error searching staff by Mobile:", e)
          return None
        finally:
           cursor.close()
    def get_staff_by_username(self, username: str):
        # conn = DBConnection.get_connection()
        cursor = self.conn.cursor(dictionary=True)

<<<<<<< HEAD
        query = "SELECT staffid, fullname, username, password, roleid, isactive FROM staffs WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        # conn.close()
        return result    
=======
    def update_staff_name(self, staff: Staff) -> bool:
        try:
          cursor = self.conn.cursor()
          query = "UPDATE staffs SET fullname = %s WHERE staffid = %s"
          values = (staff.get_fullname(), staff.get_staffid())
          cursor.execute(query, values)
          self.conn.commit()
          return True
        except Exception as e:
           print("Error updating staff name:", e)
           return False
        finally:
           cursor.close()


    def update_staff_mobileno(self, staff: Staff) -> bool:
        try:
          cursor = self.conn.cursor()
          query = "UPDATE staffs SET mobileno = %s WHERE staffid = %s"
          values = (staff.get_mobileno(), staff.get_staffid())
          cursor.execute(query, values)
          self.conn.commit()
          return True
        except Exception as e:
          print("Error updating staff mobile no:", e)
          return False
        finally:
          cursor.close()

    def disable_staff(self, staffid: int) -> bool:
        try:
          cursor = self.conn.cursor()
          query = "UPDATE staffs SET isactive = 'N' WHERE staffid = %s"
          values = (staffid,)
          cursor.execute(query, values)
          self.conn.commit()
          return True
        except Exception as e:
          print("Error disabling staff:", e)
          return False
        finally:
          cursor.close()



    
>>>>>>> adminmegha


        
      