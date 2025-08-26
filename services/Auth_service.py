from dao.StaffDaoImpl import StaffDaoImpl
from db.db_connection import get_connection

class AuthService:
    def __init__(self):
        self.staff_dao = StaffDaoImpl()

    def login(self, username: str, password: str):
        staff = self.staff_dao.get_staff_by_username(username)
        if not staff:
            return {"success": False, "message": "User not found"}

        if not staff["isactive"]:
            return {"success": False, "message": "Account inactive"}


        if password == staff["password"]:
            if staff["roleid"] == 2:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT doctorid FROM doctors WHERE staffid = %s", (staff["staffid"],))
                doctor = cursor.fetchone()
                cursor.close()
                conn.close()

                if doctor:
                    staff["doctorid"] = doctor["doctorid"]

            return {
                "success": True,
                "staffid": staff["staffid"],
                "fullname": staff["fullname"],
                "roleid": staff["roleid"],
                "doctorid": staff.get("doctorid")
            }
        else:
            return {"success": False, "message": "Invalid password"}
