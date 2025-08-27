# services/MedicineService.py

import re
from datetime import date

class MedicineService:
    @staticmethod
    def validate_medicinename(medicinename: str) -> str:
        if not medicinename or not isinstance(medicinename, str):
            raise ValueError("Medicine name cannot be empty and must be a string.")
        pattern = re.compile(r"^[A-Za-z_]{2,30}$")
        if not pattern.fullmatch(medicinename):
            raise ValueError("Medicine name must be 2–30 characters long, only letters or underscores.")
        return medicinename

    @staticmethod
    def parse_date_str(date_str: str) -> date:
        if not isinstance(date_str, str):
            raise ValueError("Date must be a string in YYYY-MM-DD format.")
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            raise ValueError("Date must follow YYYY-MM-DD format and be a valid date.")

    @staticmethod
    def validate_manufacturedate(manufacturedate: date) -> date:
        if not isinstance(manufacturedate, date):
            raise ValueError("Manufacture date must be a date object.")
        if manufacturedate > date.today():
            raise ValueError("Manufacture date cannot be in the future.")
        return manufacturedate

    @staticmethod
    def validate_expirydate(expirydate: date, manufacturedate: date) -> date:
        if not isinstance(expirydate, date):
            raise ValueError("Expiry date must be a date object.")
        if expirydate <= manufacturedate:
            raise ValueError("Expiry date must be after manufacture date.")
        return expirydate
