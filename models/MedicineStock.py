# from datetime import date, datetime

# class MedicineStock:
#     """
#     A self-contained class representing a medicine stock entry with built-in validation.
#     """

#     @staticmethod
#     def _validate_date(date_input):
#         """
#         Validates that date_input (str or date) is a valid date not in the future.
#         Raises ValueError on invalid input or wrong format.
#         """
#         if isinstance(date_input, str):
#             try:
#                 parsed = date.fromisoformat(date_input)
#             except ValueError:
#                 raise ValueError(f"Invalid date format: '{date_input}'. Expected 'YYYY-MM-DD'.")
#         elif isinstance(date_input, date):
#             parsed = date_input
#         else:
#             raise TypeError("Date must be a datetime.date or 'YYYY-MM-DD' string")

#         if parsed > date.today():
#             raise ValueError("Date cannot be in the future.")
#         return parsed

#     @staticmethod
#     def _validate_quantity(value):
#         """
#         Validates that value is a non-negative integer (accepts int or numeric string).
#         Raises ValueError otherwise.
#         """
#         try:
#             iv = int(value)
#         except (TypeError, ValueError):
#             raise ValueError(f"Quantity must be an integer, got '{value}'.")
#         if iv < 0:
#             raise ValueError("Quantity cannot be negative.")
#         return iv

#     def __init__(
#         self,
#         medicinestockid=None,
#         stockhand=0,
#         reorderlevel=0,
#         purchase=0,
#         issuance=0,
#         medicineid=None,
#         createddate=None,  # Accept as date or 'YYYY-MM-DD'
#     ):
#         self.__medicinestockid = medicinestockid
#         self.__stockhand = stockhand
#         self.__reorderlevel = reorderlevel
#         self.__purchase = purchase
#         self.__issuance = issuance
#         self.__medicineid = medicineid

#         if createddate:
#             self.__createddate = self._validate_date(createddate)
#         else:
#             self.__createddate = date.today()

#     # --- Properties with validation ---

#     @property
#     def stock_id(self):
#         return self.__medicinestockid

#     @stock_id.setter
#     def stock_id(self, value):
#         self.__medicinestockid = value

#     @property
#     def stock_hand(self):
#         return self.__stockhand

#     @stock_hand.setter
#     def stock_hand(self, value):
#         self.__stockhand = self._validate_quantity(value)

#     @property
#     def reorder_level(self):
#         return self.__reorderlevel

#     @reorder_level.setter
#     def reorder_level(self, value):
#         self.__reorderlevel = self._validate_quantity(value)

#     @property
#     def purchase(self):
#         return self.__purchase

#     @purchase.setter
#     def purchase(self, value):
#         self.__purchase = self._validate_quantity(value)

#     @property
#     def issuance(self):
#         return self.__issuance

#     @issuance.setter
#     def issuance(self, value):
#         self.__issuance = self._validate_quantity(value)

#     @property
#     def medicine_id(self):
#         return self.__medicineid

#     @medicine_id.setter
#     def medicine_id(self, value):
#         self.__medicineid = value

#     @property
#     def created_date(self):
#         return self.__createddate

#     @created_date.setter
#     def created_date(self, value):
#         self.__createddate = self._validate_date(value)

#     def __str__(self):
#         return (
#             f"StockID: {self.__stockid:<5} | "
#             f"StockHand: {self.__stockhand:<5} | "
#             f"ReorderLvl: {self.__reorderlevel:<5} | "
#             f"Purchase: {self.__purchase:<5} | "
#             f"Issuance: {self.__issuance:<5} | "
#             f"MedicineID: {self.__medicineid:<5} | "
#             f"Created: {self.__createddate}"
#         )
