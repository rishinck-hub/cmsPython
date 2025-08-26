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

            medicine.is_active = input("Is the medicine active? (Y/N): ").strip().upper()

            # Update the medicine in the database
            if MedicineManagementLib.dao_service.update(medicine):
                print("Medicine updated successfully.")
            else:
                print("Failed to update the medicine.")

    @staticmethod
    def delete_medicine():
        """Delete a medicine from the database."""
        medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to delete: ", int)
        if MedicineManagementLib.dao_service.delete(medicineid):
            print("Medicine deleted successfully.")
        else:
            print("Failed to delete the medicine.") 

    @staticmethod
    def search_medicine():
        """Search for medicines in the database."""
        query = input("Enter the medicine name or category ID to search: ")
        results = MedicineManagementLib.dao_service.search(query)
        if results:
            print("Search results:")
            for med in results:
                print(med)
        else:
            print("No medicines found.")

    @staticmethod
    def apply_gst():
        """Apply GST to a medicine."""
        medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to apply GST: ", int)
        gst_percent = MedicineManagementLib.validate_input("Enter the GST percentage: ", float)
        if MedicineManagementLib.dao_service.apply_gst(medicineid, gst_percent):
            print("GST applied successfully.")
        else:
            print("Failed to apply GST.")

    @staticmethod
    def disable_medicine():
        """Disable a medicine in the database."""
        medicineid = MedicineManagementLib.validate_input("Enter the medicine ID to disable: ", int)
        if MedicineManagementLib.dao_service.disable(medicineid):
            print("Medicine disabled successfully.")
        else:
            print("Failed to disable the medicine.")
