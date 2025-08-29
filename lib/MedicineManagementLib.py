from turtle import update
from dao.MedicineDaoImpl import MedicineDaoDb
from dao.MedicineStockDaoImpl import MedicineStockDaoDb
from models.Medicine import Medicine
from models.MedicineStock import MedicineStock  
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

    @staticmethod
    def search_medicine():
        """Search for medicines in the database."""
        query = input("Enter the medicine name or Medicine ID to search: ")
        results = MedicineManagementLib.dao_service.search(query)

        if results:
            print("Search results:")
            for med in results:
                print(med)
        else:
            print("No medicines found.")

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

class MedicineStockManagementLib:
    dao_service: MedicineStockDaoDb = MedicineStockDaoDb()

    @staticmethod
    def add_stock():
        """Add a new stock entry to the database with proper validations."""

        # Get and validate inputs
        stockhand = MedicineStockManagementLib.validate_input("Enter stock hand quantity: ", int)
        reorderlevel = MedicineStockManagementLib.validate_input("Enter reorder level: ", int)
        purchase = MedicineStockManagementLib.validate_input("Enter purchase quantity: ", int)
        issuance = MedicineStockManagementLib.validate_input("Enter issuance quantity: ", int)
        medicineid = MedicineStockManagementLib.validate_input("Enter associated medicine ID: ", int)

        # Optional: default to current date if createddate not entered
        createddate_input = input("Enter created date (YYYY-MM-DD) or leave blank for today: ").strip()
        if createddate_input:
            try:
                createddate = datetime.strptime(createddate_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                return
        else:
            createddate = datetime.today().date()

        # Generate a stock ID (adjust logic as needed)
        

        # Create MedicineStock object
        stock = MedicineStock(
            stockhand=stockhand,
            reorderlevel=reorderlevel,
            purchase=purchase,
            issuance=issuance,
            medicineid=medicineid,
            createddate=createddate
        )

        # Attempt insert
        if MedicineStockManagementLib.dao_service.insert(stock):
            print("Stock added successfully.")
        else:
            print("Failed to add the stock.")

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
    def update_stock():
        """Update an existing stock entry in the database."""
        stock_id = MedicineStockManagementLib.validate_input("Enter the stock ID to update: ", int)
        stock = MedicineStockManagementLib.dao_service.find_by_id(stock_id)

        if not stock:
            print("Stock not found.")
            return


        print("Current stock details:", stock)
        confirm = input("Do you want to update this stock? (Y/N): ").strip().lower()

        if confirm != 'y':

            print("Update cancelled.")
            return

        # Prompt for new values—example uses generic attribute names
        new_stockhand = MedicineStockManagementLib.validate_input(
            "Enter new stockhand (leave blank to keep current): "#, int, allow_empty=True
        )
        new_reorderlevel = MedicineStockManagementLib.validate_input(
            "Enter new reorderlevel (leave blank to keep current): "#, int, allow_empty=True
        )
        new_purchase = MedicineStockManagementLib.validate_input(
            "Enter new purchase (leave blank to keep current): "#, int, allow_empty=True
        )
        new_issuance = MedicineStockManagementLib.validate_input(
            "Enter new issuance (leave blank to keep current): "#, int, allow_empty=True
        )

        # Update only the values the user provided
        updates = {}
        if new_stockhand is not None:
            updates['stockhand'] = new_stockhand
        if new_reorderlevel is not None:
            updates['reorderlevel'] = new_reorderlevel
        if new_purchase is not None:
            updates['purchase'] = new_purchase
        if new_issuance is not None:
            updates['issuance'] = new_issuance

        if not updates:
            print("No changes entered. Update aborted.")
            return

        try:
            MedicineStockManagementLib.dao_service.update(stock_id, **update)
            print("Stock updated successfully.")
        except Exception as e:
            print(f"Failed to update stock: {e}")

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
    @staticmethod
    def display_all_stock():
        """Display all stock entries."""
        stock_entries = MedicineStockManagementLib.dao_service.display_all_stock()
        if stock_entries:
            for stock in stock_entries:
                print(stock)
        else:
            print("No stock entries found.")