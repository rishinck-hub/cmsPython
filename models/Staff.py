from datetime import datetime,date
import re
class Staff:
    def __init__(self,staffid=None,fullname=None,gender=None,bloodgroup=None,
                 mobileno=None,dob=None,username=None,password=None,roleid=None,
                 isactive=None):
        self.__staffid = staffid
        self.__fullname = fullname
        self.__gender = gender
        self.__bloodgroup = bloodgroup
        self.__mobileno = mobileno
        self.__dob = dob
        self.__username = username
        self.__password = password
        self.__roleid = roleid
        self.__isactive = isactive

    def get_staffid(self):
        return self.__staffid
    def set_staffid(self,staffid):
        self.__staffid = staffid

    def get_fullname(self):
        return self.__fullname
    def set_fullname(self,fullname):
        pattern = re.compile(r"^[A-Za-z_]{3,30}$")

        while True:
            if pattern.match(fullname):
                self.__fullname = fullname
                break
            else:
                print("\t\t Name should have atleast 3 characters")
                fullname = input(" Enter Full Name again:")

    def get_gender(self):
        return self.__gender
    def set_gender(self, gender):
        gender = gender.lower()  # normalize
        if gender in ("male", "female","other"):
          self.__gender = gender
        else:
          print("Invalid gender! Please enter 'male' or 'female'.")
          gender = input("Enter Gender again (male/female):")

    def get_bloodgroup(self):
        return self.__bloodgroup
    def set_bloodgroup(self, bloodgroup):
        valid_bloodgroups = {"A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"}
        bloodgroup = bloodgroup.upper()  # normalize
        if bloodgroup in valid_bloodgroups:
          self.__bloodgroup = bloodgroup
        else:
          print("Invalid blood group! Please enter one of:", ", ".join(valid_bloodgroups))
          bloodgroup = input("Enter Blood Group again:")

    def get_mobileno(self):
        return self.__mobileno
    def set_mobileno(self, mobileno):
    # Mobile should start with 6-9 and have exactly 10 digits
        if re.fullmatch(r"[6-9]\d{9}", str(mobileno)):
           self.__mobileno = mobileno
        else:
           print("Invalid mobile number! It must start with 6-9 and have exactly 10 digits.")
           mobileno = input("Enter mobile no again:")

    def get_dob(self):
        return self.__dob
    def set_dob(self, dob:str):
        if self.__validate_date(dob):
          dob = datetime.strptime(dob, "%d/%m/%Y").date()
          age = self.__calculate_age(dob)

          if 18 <= age <= 60:
            self.__dob = dob
          else:
            print("Invalid DOB! Age must be between 18 and 60 years.")
            dob = input("Enter dob again:")
            return
        else:
           print("Give the date in the correct format (dd/mm/yyyy)")
           return

    def __validate_date(self, date_str: str) -> bool:
        try:
          datetime.strptime(date_str, "%d/%m/%Y")
          return True
        except ValueError:
           return False

    def __calculate_age(self, dob):
        today = datetime.today().date()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age


    def get_username(self):
        return self.__username
    def set_username(self, username):
        if len(username) >= 6:
            self.__username = username
        else:
            print("Username should have at least 6 characters")
            username = input("Enter username again:")

    def get_password(self):
        return self.__password
    def set_password(self, password):
        if len(password) >= 6:
            self.__password = password
        else:
            print("Password should have at least 6 characters")
            password = input("Enter password again:")

    def get_roleid(self):
        return self.__roleid
    def set_roleid(self, roleid):
        self.__roleid = roleid


    def get_isactive(self):
        return self.__isactive
    def set_isactive(self, isactive):
        self.__isactive = isactive

    def __str__(self):
     return (
        f"Staff ID    : {self.__staffid}\n"
        f"Full Name   : {self.__fullname}\n"
        f"Gender      : {self.__gender}\n"
        f"Blood Group : {self.__bloodgroup}\n"
        f"Mobile No   : {self.__mobileno}\n"
        f"DOB         : {self.__dob}\n"
        f"UserName    : {self.__username}\n"
        f"Password    : {self.__password}\n"
        f"Role ID     : {self.__roleid}\n"
        f"Is Active   : {self.__isactive}"
    )

    
    
  

        