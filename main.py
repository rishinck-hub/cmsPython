from db.db_connection import DBConnection
from  lib.MedicineManagementLib import MedicineManagementLib
def main():
    while True:
        # db = DBConnection()
        # conn = db.get_connection()
        print("\n==========MEDICINE MANAGEMENT MENU==========")
        print("|1. Add Medicine                              |")
        print("|2. Display all Medicine                      |")
        print("|3. Update Medicine                           |")
        print("|4. Search Medicine                           |")
        print('|5. Apply GST to Medicine                     |')
        print('|6. Disable Medicine                          |')
        print('|7. Delete Medicine                           |')
        print('|8. exit                                      |')
        print('-----------------------------------------------')
        choice = input("Enter your choice : ")
        if choice == "1":
            MedicineManagementLib.add_medicine()
        elif choice == "2":
            MedicineManagementLib.display_all()
        elif choice == "3":
            MedicineManagementLib.update_medicine()
        elif choice == "4":
            MedicineManagementLib.search_medicine()
        elif choice == '5':
            MedicineManagementLib.apply_gst()
        elif choice == '6':
            MedicineManagementLib.disable_medicine()
        elif choice == '7':
            MedicineManagementLib.delete_medicine()
        elif choice == '8':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice!! Try again!!")
        
if __name__ == "__main__":
    main()
