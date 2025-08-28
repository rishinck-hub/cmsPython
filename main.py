# from lib.LoginManagementLib import LoginManagementLib

# if __name__ == "__main__":
#     print("=== Clinic Management System ===")
#     LoginManagementLib.login()
#from models import MedicineStock

from db.db_connection import DBConnection
from  lib.MedicineManagementLib import MedicineManagementLib
from lib.MedicineManagementLib import MedicineStockManagementLib   
def main():
    while True:
        # db = DBConnection()
        # conn = db.get_connection()
        print("\n==========MEDICINE MANAGEMENT MENU==========")
        print("|1. Add Medicine                              |")
        print("|2. Display all Medicine                      |")
        print("|3. Update Medicine                           |")
        print("|4. delete Medicine                           |")
        print('|5. search to Medicine                        |')
        print('|6. Add stock                                 |')
        print('|7. Display stock                             |')
        print('|8. Update stock                              |')
        print('|9. Exit                                      |')
        print('-----------------------------------------------')
        choice = input("Enter your choice : ")
        if choice == "1":
            MedicineManagementLib.add_medicine()
        elif choice == "2":
            MedicineManagementLib.display_all()
        elif choice == "3":
            MedicineManagementLib.update_medicine()
        elif choice == "4":
            MedicineManagementLib.delete_medicine()
        elif choice == '5':
            MedicineManagementLib.search_medicine()
        elif choice == '6':
            MedicineStockManagementLib.add_stock()
        elif choice == '7':
            MedicineStockManagementLib.display_all_stock()
        elif choice == '8':
            MedicineStockManagementLib.update_stock()
            

        elif choice == '9':
            print("Exiting the program.")
            break
if __name__ == "__main__":
<<<<<<< HEAD
    print("=== Clinic Management System ===")
    while True:
        print('1.Login')
        print('2.Exit')
        choice = input("Enter your choice :")
        if choice =='1':
                LoginManagementLib.login()
        elif choice =='2':
             print('Exiting...')
             break
        else:
             print('Invalid choice')             
=======
    main()
>>>>>>> teammember
