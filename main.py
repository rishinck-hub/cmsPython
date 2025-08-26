from db.db_connection import DBConnection
from lib.staffManagementLib import StaffManagementLib

def main():
    while True:
           print("\n=============STAFF MANAGEMENT MENU==============")
           print("1. ADD STAFF")
           print("2. SEE LIST OF STAFFS")
           print("3. SEARCH AND VIEW STAFF")
           print("4. GO TO MAIN MENU")
           choice = input("Enter your choice:")
           if choice == "1":
                StaffManagementLib.add_staff()
           elif choice == "2":
                StaffManagementLib.display_all()
           elif choice == "3":
                print("\n========= Search Staff Menu =========")
                print("1. By Staff Number")
                print("2. By Phone Number")
                print("3. Go Back")

                search_choice = input("Enter your choice (1-3): ")

                staff = None
                if search_choice == "1":
                 staff = StaffManagementLib.search_by_staffid()
                elif search_choice == "2":
                  staff = StaffManagementLib.search_by_mobileno()
                elif search_choice == "3":
                  continue
                else:
                  print(" Invalid choice! Please enter 1, 2, or 3.")
                  continue

                if staff:  # staff found
                   print(f"\nStaff Found: {staff.get_fullname()} ({staff.get_mobileno()})")

                   while True:
                       print("\n========= Staff Action Menu =========")
                       print("1. Edit Staff")
                       print("2. Disable Staff")
                       print("3. Go Back")

                       action_choice = input("Enter your choice (1-3): ")
                       if action_choice == "1":
                        StaffManagementLib.edit_staff_name(staff)
                        break
                       elif action_choice == "2":
                        StaffManagementLib.disable_staff(staff)
                        break
                       elif action_choice == "3":
                        break
                       else:
                        print(" Invalid choice. Try again.")
           elif choice == "4":
             break
           else:
             print(" Invalid choice, try again!")

def edit_staff_menu(staff):
    while True:
        print("\n========= Edit Staff Menu =========")
        print("1. Name")
        print("2. Go Back")

        choice = input("Which field do you want to edit? (1-2): ")

        if choice == "1":
            new_name = input("Enter new Name: ")
            StaffManagementLib.update_staff_name(staff, new_name)

        elif choice == "2":
            break

        else:
            print(" Invalid choice. Try again.")

         

                    

if __name__ == '__main__':
    main()