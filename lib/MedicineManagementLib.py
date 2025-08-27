from dao.MedicineDaoImpl import MedicineDaoDb
from models.Medicine import Medicine
from datetime import datetime

class MedicineManagementLib:
    """
    Class to manage medicines and interact with the database through the MedicineDaoDb.
    """
    dao_service: MedicineDaoDb = MedicineDaoDb()

    @staticmethod
    def display_all():
        """Display all medicines stored in the database."""
        medicines = MedicineManagementLib.dao_service.display_all()
        if medicines:
            for med in medicines:
                print(med)
        else:
            print("No medicines available.")

    @staticmethod
    def validate_input(prompt, input_type=str, is_required=True):
        """Helper function to validate inputs (string, numeric, etc.)"""
        while True:
            try:
                user_input = input(prompt).strip()
                if is_required and not user_input:
                    raise ValueError("This field cannot be empty.")
                
                if input_type == str:
                    return user_input
                elif input_type == float:
                    return float(user_input)
                elif input_type == int:
                    return int(user_input)
                else:
                    raise ValueError(f"Unsupported input type {input_type}")
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    @staticmethod
    def add_medicine():
        """Add a new medicine to the database with proper validations."""
        # Prompt for and validate the medicine name first
        name = input("Enter the medicine name: ").strip()
        
        # Validate the medicine name is not empty and a valid string
        if not name or not isinstance(name, str):
            print("Error: Medicine name cannot be empty and must be a string.")
            return

        # Initialize the Medicine instance after validating name
        medicine = Medicine()
        try:
            medicine.medicinename = name  # This will trigger the setter validation
        except ValueError as e:
            print("Invalid medicine name:", e)
            return

        # Validate numeric inputs
        try:
            medicine.unitprice = float(input("Enter the unit price: ").strip())
            medicine.unitquantiy = int(input("Enter the unit quantity: ").strip())
            medicine.unitid = int(input("Enter the unit ID: ").strip())
            medicine.medicinecategoryid = int(input("Enter the category ID: ").strip())
        except ValueError as e:
            print("Invalid numeric input:", e)
            return

        # Validate date inputs
        m_date = input("Enter manufacture date (YYYY-MM-DD): ").strip()
        e_date = input("Enter expiry date (YYYY-MM-DD): ").strip()
        try:
            medicine.manufacturedate = datetime.strptime(m_date, "%Y-%m-%d").date()
            medicine.expirydate = datetime.strptime(e_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return


        # Attempt database insert
        if MedicineManagementLib.dao_service.insert(medicine):
            print("Medicine added successfully.")
        else:
            print("Failed to add the medicine.")

    @staticmethod
    def find_by_id():
        """View details of a specific medicine."""
        medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to view: ", int)
        medicine = MedicineManagementLib.dao_service.find_by_id(medicineid)
        if medicine:
            print("Medicine details:")
            print(medicine)
        else:
            print("Medicine not found.")

    @staticmethod
    def update_medicine():
        """Update an existing medicine in the database."""
        search_id = MedicineManagementLib.validate_input("Enter the medicine ID to update: ", int)
        medicine = MedicineManagementLib.dao_service.find_by_id(search_id)

        if not medicine:
            print("Medicine not found.")
            return

        print("Current medicine details:", medicine)
        confirm = input("Do you want to update this medicine? (Y/N): ").strip().lower()

        if confirm == 'y':
            medicine.medicinename = input("Enter new medicine name: ")
            medicine.unitprice = MedicineManagementLib.validate_input("Enter new unit price: ", float)
            medicine.unitquantiy = MedicineManagementLib.validate_input("Enter new unit quantity: ", int)
            medicine.unitid = MedicineManagementLib.validate_input("Enter new unit ID: ", int)
            medicine.medicinecategoryid = MedicineManagementLib.validate_input("Enter new category ID: ", int)

            # Handle the manufacture and expiry dates
            m_date = input(f"Enter new manufacture date (YYYY-MM-DD) (Current: {medicine.manufacturedate}): ")
            e_date = input(f"Enter new expiry date (YYYY-MM-DD) (Current: {medicine.expirydate}): ")

            try:
                # Parse dates to datetime objects
                if m_date:
                    manufacturedate = datetime.strptime(m_date, "%Y-%m-%d").date()
                    medicine.manufacturedate = manufacturedate
                if e_date:
                    expirydate = datetime.strptime(e_date, "%Y-%m-%d").date()
                    medicine.expirydate = expirydate
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                return

            

            # Update the medicine in the database
            if MedicineManagementLib.dao_service.update(medicine, medicine.medicine_id):
                print("Medicine updated successfully.")
            else:
                print("Failed to update the medicine.")

    @staticmethod
    # def delete_medicine():
    #     """Delete a medicine from the database."""
    #     medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to delete: ", int)
    #     if MedicineManagementLib.dao_service.delete(medicineid):
    #         print("Medicine deleted successfully.")
    #     else:
    #         print("Failed to delete the medicine.") 

    @staticmethod
    def bill_medicine():
        """Bill a specific medicine."""
        medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to bill: ", int)
        quantity = MedicineManagementLib.validate_input("Enter the quantity: ", int)
        if MedicineManagementLib.dao_service.bill(medicineid, quantity):
            print("Medicine billed successfully.")
        else:
            print("Failed to bill the medicine.")

    def delete_medicine():
        medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to delete: ", int)
        if MedicineManagementLib.dao_service.delete(medicineid):
            print("Medicine deleted successfully.")
        else:
            print("Failed to delete the medicine.")

    # @staticmethod
    # def search_medicine():
    #     """Search for medicines in the database."""
    #     query = input("Enter the medicine name or category ID to search: ")
    #     results = MedicineManagementLib.dao_service.search(query)
    #     if results:
    #         print("Search results:")
    #         for med in results:
    #             print(med)
    #     else:
    #         print("No medicines found.")

    # @staticmethod
    # def apply_gst():
    #     """Apply GST to a medicine."""
    #     medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to apply GST: ", int)
    #     gst_percent = MedicineManagementLib.validate_input("Enter the GST percentage: ", float)
    #     if MedicineManagementLib.dao_service.apply_gst(medicineid, gst_percent):
    #         print("GST applied successfully.")
    #     else:
    #         print("Failed to apply GST.")

    # @staticmethod
    # def disable_medicine():
    #     """Disable a medicine in the database."""
    #     medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to disable: ", int)
    #     if MedicineManagementLib.dao_service.disable(medicineid):
    #         print("Medicine disabled successfully.")
    #     else:
    #         print("Failed to disable the medicine.")

# class MedicineStockManagementLib:
#     @staticmethod
#     def add_stock():
#         """Add a new stock entry to the database with proper validations."""
#         # Prompt for and validate the medicine ID
#         medicinestockid = MedicineStockManagementLib.validate_input(
#             "Enter the medicine stock ID: ", input_type=int)

#         # Validate the batch number (string)
#         stockhand = input("Enter the batch stockhand: ").strip()
#         if not stockhand:
#             print("Error: Batch stockhand cannot be empty.")
#             return
        
#         # Validate numeric inputs (reorderlevel)
#         try:
#             reorderlevel = int(input("Enter the reorderlevel: ").strip())
#         except ValueError as e:
#             print("Invalid reorderlevel input:", e)
#             return

#         # Validate date inputs (stock date and expiry date)
#         purchase = input("Enter stock date (YYYY-MM-DD): ").strip()
#         expiry_date = input("Enter expiry date (YYYY-MM-DD): ").strip()
#         try:
#             stock_date = datetime.strptime(stock_date, "%Y-%m-%d").date()
#             expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
#         except ValueError:
#             print("Invalid date format. Please use YYYY-MM-DD.")
#             return

#         # Initialize the MedicineStock instance after validating the inputs
#         stock = MedicineStock()
#         stock.medicineid = medicine_id
#         stock.batchnumber = batch_number
#         stock.quantity = quantity
#         stock.stockdate = stock_date
#         stock.expirydate = expiry_date

#         # Attempt database insert
#         if MedicineStockManagementLib.dao_service.insert(stock):
#             print("Stock added successfully.")
#         else:
#             print("Failed to add the stock.")

#     @staticmethod
#     def update_stock():
#         """Update an existing stock entry in the database."""
#         stock_id = MedicineStockManagementLib.validate_input(
#             "Enter the stock ID to update: ", input_type=int)
        
#         # Find the stock record by ID
#         stock = MedicineStockManagementLib.dao_service.find_by_id(stock_id)
#         if not stock:
#             print("Stock record not found.")
#             return
        
#         print(f"Updating stock: {stock}")

#         # Validate and update the quantity, batch number, and expiry date
#         quantity = MedicineStockManagementLib.validate_input("Enter new quantity: ", input_type=int, is_required=False)
#         batch_number = input("Enter new batch number: ").strip() or stock.batchnumber
#         expiry_date = input("Enter new expiry date (YYYY-MM-DD): ").strip() or str(stock.expirydate)
        
#         try:
#             expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
#         except ValueError:
#             print("Invalid expiry date format. Please use YYYY-MM-DD.")
#             return

#         # Update stock fields
#         stock.quantity = quantity if quantity else stock.quantity
#         stock.batchnumber = batch_number
#         stock.expirydate = expiry_date

#         # Attempt database update
#         if MedicineStockManagementLib.dao_service.update(stock, stock_id):
#             print("Stock updated successfully.")
#         else:
#             print("Failed to update the stock.")

#     @staticmethod
#     def disable_stock():
#         """Disable a stock entry in the database."""
#         stock_id = MedicineStockManagementLib.validate_input(
#             "Enter the stock ID to disable: ", input_type=int)

#         # Attempt to disable the stock entry
#         if MedicineStockManagementLib.dao_service.disable(stock_id):
#             print("Stock disabled successfully.")
#         else:
#             print("Failed to disable the stock.")
    
#     @staticmethod
#     def search_stock():
#         """Search for stock based on batch number or medicine ID."""
#         query = input("Enter search query (batch number or medicine ID): ").strip()
        
#         # Perform search
#         stock_entries = MedicineStockManagementLib.dao_service.search(query)
#         if stock_entries:
#             for stock in stock_entries:
#                 print(stock)
#         else:
#             print("No stock entries found for the search query.")