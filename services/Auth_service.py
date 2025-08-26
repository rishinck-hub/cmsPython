from dao.StaffDaoImpl import StaffDaoImplementation
from db.db_connection import DBConnection

class AuthService:
    def __init__(self):
        self.staff_dao = StaffDaoImplementation()

    def login(self, username: str, password: str):
        staff = self.staff_dao.get_staff_by_username(username)
        if not staff:
            return {"success": False, "message": "User not found"}

        if not staff["isactive"]:
            return {"success": False, "message": "Account inactive"}

        # 🔑 Plain-text password check
        if password == staff["password"]:
            # If doctor, also fetch doctorid
            if staff["roleid"] == 2:
                conn = DBConnection.get_connection()
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
