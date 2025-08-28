from dao.LoginDao import LoginDaoService
from db.db_connection import DBConnection
from typing import List
from models.Staff import Staff
from datetime import date,datetime

class LoginDaoImplementation(LoginDaoService):

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def get_staff_by_username(self, username: str):
        # conn = DBConnection.get_connection()
        cursor = self.conn.cursor(dictionary=True)

        query = "SELECT staffid, fullname, username, password, roleid, isactive FROM staffs WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        cursor.close()
        # conn.close()
        return result   