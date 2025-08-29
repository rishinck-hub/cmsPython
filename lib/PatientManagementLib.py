import re
from datetime import datetime

class PatientManagementLib:
    @staticmethod
    def validate_name(name):
        """Validate patient name - alphabetic characters only, minimum 3 characters, no multiple spaces"""
        if not name or not isinstance(name, str):
            return False
        stripped = name.strip()
        # Check for multiple consecutive spaces
        if '  ' in stripped:
            return False
        # Allow spaces and hyphens in names
        return bool(re.match(r'^[a-zA-Z\s\-]+$', stripped)) and len(stripped) >= 3

    @staticmethod
    def validate_mobile(mobile):
        """Validate mobile number - 10 digits, starts with 6/7/8/9"""
        if not mobile or not isinstance(mobile, str):
            return False
        return bool(re.match(r'^[6-9]\d{9}$', mobile.strip()))

    @staticmethod
    def validate_dob(dob):
        """Validate date of birth format and reasonable age range"""
        if not dob or not isinstance(dob, str):
            return False
        try:
            date_obj = datetime.strptime(dob, '%Y-%m-%d')
            current_date = datetime.now()
            
            # Check if date is not in the future
            if date_obj > current_date:
                return False
            
            # Check if age is reasonable (between 0 and 120 years)
            age = current_date.year - date_obj.year
            if age < 0 or age > 120:
                return False
                
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_gender(gender):
        """Validate gender - Male, Female, Other (accepts M/F/O too)"""
        if not gender or not isinstance(gender, str):
            return False
        valid_genders = ['male', 'female', 'other']
        return gender.lower() in valid_genders

    @staticmethod
    def validate_bloodgroup(bloodgroup):
        """Validate blood group - A+/-, B+/-, AB+/-, O+/-"""
        if not bloodgroup or not isinstance(bloodgroup, str):
            return False
        valid = {"A+","A-","B+","B-","AB+","AB-","O+","O-"}
        return bloodgroup.strip().upper() in valid

    @staticmethod
    def validate_address(address):
        """Validate address - non-empty string with reasonable length, no multiple spaces"""
        if not address or not isinstance(address, str):
            return False
        stripped = address.strip()
        # Check for multiple consecutive spaces
        if '  ' in stripped:
            return False
        return 5 <= len(stripped) <= 200

    @staticmethod
    def validate_patient_id(patient_id):
        """Validate patient ID - positive integer"""
        try:
            patient_id_int = int(patient_id)
            return patient_id_int > 0
        except (ValueError, TypeError):
            return False
