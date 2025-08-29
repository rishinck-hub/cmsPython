import re
from decimal import Decimal, InvalidOperation

class BillingManagementLib:
    @staticmethod
    def validate_amount(amount):
        """
        Validate monetary amount
        - Must be a positive number
        - Can have up to 2 decimal places
        """
        if not amount or not isinstance(amount, (int, float, str, Decimal)):
            return False
            
        try:
            # Convert to Decimal for precise decimal arithmetic
            amount_decimal = Decimal(str(amount))
            
            # Check if amount is positive
            if amount_decimal <= 0:
                return False
                
            # Check if it has more than 2 decimal places
            if abs(amount_decimal.as_tuple().exponent) > 2:
                return False
                
            return True
            
        except (ValueError, InvalidOperation):
            return False

    @staticmethod
    def validate_prescription_id(prescription_id):
        """
        Validate prescription ID
        - Must be a positive integer or None
        """
        if prescription_id is None:
            return True
            
        try:
            return int(prescription_id) > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_consultation_fee(fee):
        """
        Validate consultation fee
        - Must be a non-negative number
        - Can have up to 2 decimal places
        """
        if fee is None or not isinstance(fee, (int, float, str, Decimal)):
            return False
            
        try:
            fee_decimal = Decimal(str(fee))
            
            # Check if amount is non-negative
            if fee_decimal < 0:
                return False
                
            # Check if it has more than 2 decimal places
            if abs(fee_decimal.as_tuple().exponent) > 2:
                return False
                
            return True
            
        except (ValueError, InvalidOperation):
            return False

    @staticmethod
    def validate_billing_date(date_str, date_format='%Y-%m-%d'):
        """
        Validate billing date format
        - Default format: YYYY-MM-DD
        - Must be a valid date not in the future
        """
        from datetime import datetime
        
        if not date_str or not isinstance(date_str, str):
            return False
            
        try:
            date_obj = datetime.strptime(date_str, date_format)
            current_date = datetime.now()
            
            # Check if date is not in the future
            return date_obj.date() <= current_date.date()
            
        except ValueError:
            return False

    @staticmethod
    def validate_patient_id(patient_id):
        """
        Validate patient ID
        - Must be a positive integer
        """
        try:
            return int(patient_id) > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_appointment_id(appointment_id):
        """
        Validate appointment ID
        - Must be a positive integer
        """
        try:
            return int(appointment_id) > 0
        except (ValueError, TypeError):
            return False
